# API Parque de Diversiones

API REST construida con FastAPI, SQLAlchemy y PostgreSQL
cd "C:\Users\Castr\OneDrive\Escritorio\ISW_2025_4K3_G12\Entregas\Trabajos_Practicos\TP06_Test Driven Development (TDD)\Back"

## Inicio Rápido

Para iniciar el servidor FastAPI:

**En la terminal integrada de VS Code (recomendado):**
```bash
# 1. Activar entorno virtual
source venv/Scripts/activate  # Windows
# 2. Ejecutar el script
./start_services.sh
```

**Nota:** El script asume que el entorno virtual ya está activado en la terminal actual.

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

4. **Crear base de datos**
   - Crear la base de datos `parque_db` en PostgreSQL
   - **Importante para Windows**: Asegúrate de que PostgreSQL esté corriendo como servicio

5. **Ejecutar migraciones**
   ```bash
   alembic upgrade head
   ```

7. **Acceder a la API**
   - API: http://localhost:8080
   - Documentación: http://localhost:8080/docs
