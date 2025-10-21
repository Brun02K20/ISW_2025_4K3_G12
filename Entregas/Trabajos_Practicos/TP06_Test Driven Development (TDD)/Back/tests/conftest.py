# tests/conftest.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.domain.database import Base, get_db
from src.application.main import app

# --- STEP 1: Fixture to create the Engine ---
# This runs only ONCE per test session and delays creation
@pytest.fixture(scope="session")
def db_engine():
    """Fixture that creates the database engine for tests."""
    print("\n--- Creating Test DB Engine ---") # Debug print
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "admin")
    # This getenv() now runs later, inside the fixture
    db_host = os.getenv("DB_HOST", "localhost") # Should read 'postgres_db'
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "parque_db")

    print(f"--- Connecting test engine to host: {db_host} ---") # Debug print

    test_database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    try:
        engine = create_engine(test_database_url)
        # Verify connection works before creating tables
        with engine.connect() as connection:
             print("--- Test DB Engine connection successful ---") # Debug print
        # Create tables once for the test session
        Base.metadata.create_all(bind=engine)
        print("--- Test DB tables created ---") # Debug print
        yield engine
    except Exception as e:
        print(f"--- !!! ERROR CREATING TEST DB ENGINE: {e} !!! ---") # Debug print
        pytest.fail(f"Failed to create test DB engine: {e}")
    finally:
        # Optional cleanup at the very end
        # Base.metadata.drop_all(bind=engine)
        print("--- Test DB Engine fixture finished ---") # Debug print
        pass

# --- STEP 2: Fixture for the DB Session, depending on the engine ---
# This runs for EACH test function
@pytest.fixture(scope="function")
def db_session(db_engine): # <-- Depends on the db_engine fixture
    """Fixture that creates a DB session for each test and handles transactions."""

    # Get the engine created by the fixture
    connection = db_engine.connect()
    # Begin a transaction
    transaction = connection.begin()

    # Create a session bound to this connection
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    db = TestingSessionLocal()

    try:
        yield db # The test runs here
    finally:
        db.close()
        # Roll back the transaction, undoing any changes made by the test
        transaction.rollback()
        connection.close()
        # print("--- Test DB Session closed and rolled back ---") # Uncomment for verbose logs

# --- STEP 3: Client Fixture depends on the new db_session ---
@pytest.fixture(scope="function")
def client(db_session): # <-- Depends on the corrected db_session
    """Fixture to create a FastAPI TestClient."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass # Session cleanup is handled by db_session fixture

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    # Clean up override after test client finishes
    del app.dependency_overrides[get_db]