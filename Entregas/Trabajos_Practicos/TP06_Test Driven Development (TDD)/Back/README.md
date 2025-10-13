# API Parque de Diversiones

API REST construida con FastAPI, SQLAlchemy y PostgreSQL para la gestión de un parque de diversiones.

## Arquitectura del Proyecto

```
Back/
├── src/
│   ├── domain/                    # Lógica de negocio (Domain Layer)
│   │   ├── models.py             # Modelos de datos (SQLAlchemy)
│   │   ├── schemas.py            # Esquemas Pydantic
│   │   ├── database.py           # Configuración de base de datos
│   │   └── services/             # Servicios de negocio
│   │       ├── inscripcion_service.py
│   │       └── ... (otros servicios)
│   ├── infrastructure/           # Interfaces externas (Infrastructure Layer)
│   │   └── routers/              # Endpoints de la API
│   │       ├── parque.py
│   │       ├── actividad.py
│   │       └── ... (otros routers)
│   └── application/              # Punto de entrada (Application Layer)
│       └── main.py               # Aplicación FastAPI
├── tests/                        # Tests (fuera de src/)
│   ├── test_inscripcion.py
│   └── conftest.py
├── alembic/                      # Migraciones de base de datos
├── requirements.txt              # Dependencias
├── start_services.sh             # Script de inicio
└── README.md
```

## Inicio Rápido

Para iniciar el servidor FastAPI:

**En la terminal integrada de VS Code (recomendado):**
```bash
# 1. Activar entorno virtual
venv/Scripts/activate  # Desde Windows Powershell
# o
source venv/bin/activate     # Linux/Mac

# 2. Ejecutar el script
./start_services.sh
```

**O directamente:**
```bash
source venv/Scripts/activate
uvicorn src.application.main:app --host 0.0.0.0 --port 8080 --reload
```

## Instalación Detallada

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd TP06_Test\ Driven\ Development\ \(TDD\)/Back
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # Windows (Git Bash) o Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Crear base de datos**
   - Crear la base de datos `parque_db` en PostgreSQL
   - **Importante para Windows**: Asegúrate de que PostgreSQL esté corriendo como servicio

6. **Ejecutar migraciones**
   ```bash
   alembic upgrade head
   ```

7. **Acceder a la API**
   - API: http://localhost:8080
   - Documentación: http://localhost:8080/docs

## Desarrollo

- **Domain Layer** (`src/domain/`): Contiene la lógica de negocio pura, independiente de frameworks
- **Infrastructure Layer** (`src/infrastructure/`): Interfaces externas (APIs, bases de datos)
- **Application Layer** (`src/application/`): Punto de entrada y configuración
- **Tests** (`tests/`): Tests unitarios e integración siguiendo TDD

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **Alembic**: Migraciones de base de datos
- **PostgreSQL**: Base de datos relacional
- **Pydantic**: Validación de datos
- **pytest**: Framework de testing
- **python**: lenguaje de programacion. version version = 3.12.6
