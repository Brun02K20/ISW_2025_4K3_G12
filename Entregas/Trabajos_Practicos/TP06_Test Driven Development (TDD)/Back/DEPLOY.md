# Guía de Despliegue en VPS Ubuntu 22.04

Esta guía describe el proceso completo para desplegar la aplicación FastAPI con PostgreSQL en un servidor VPS Ubuntu 22.04 utilizando Docker y Docker Compose.

---

## 📋 Requisitos Previos

- VPS con Ubuntu 22.04 LTS
- Acceso SSH al servidor
- Dominio o IP pública configurada (opcional)
- Git instalado en el servidor

---

## 🚀 Proceso de Despliegue

### 1. Conexión Inicial al VPS

```bash
ssh usuario@tu-vps-ip
```

**Nota:** Reemplazá `usuario` y `tu-vps-ip` con tus credenciales reales.

---

### 2. Actualización del Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

---

### 3. Instalación de Docker

#### Opción A: Docker desde repositorios oficiales (Recomendado)

```bash
# Instalar dependencias necesarias
sudo apt install -y ca-certificates curl gnupg lsb-release

# Agregar la clave GPG oficial de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar el repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Actualizar índice de paquetes
sudo apt update

# Instalar Docker Engine, containerd y Docker Compose plugin
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Opción B: Docker desde repositorios de Ubuntu (Si Opción A falla)

```bash
sudo apt install -y docker.io
```

---

### 4. Configuración de Docker

```bash
# Iniciar el servicio Docker
sudo systemctl start docker

# Habilitar Docker para que inicie automáticamente
sudo systemctl enable docker

# Verificar el estado
sudo systemctl status docker

# Agregar tu usuario al grupo docker (evita usar sudo)
sudo usermod -aG docker $USER
```

**⚠️ Importante:** Después de agregar tu usuario al grupo docker, **debes cerrar sesión y reconectarte** para que los cambios surtan efecto.

```bash
exit
# Reconectate por SSH
ssh usuario@tu-vps-ip
```

---

### 5. Verificar Instalación de Docker

```bash
# Verificar versión de Docker
docker --version

# Verificar Docker Compose (plugin)
docker compose version

# Test básico de Docker (opcional)
docker run hello-world
```

**Nota:** Si instalaste Docker Engine oficial, usá `docker compose` (sin guión). Si instalaste `docker.io`, podés necesitar `docker-compose` (con guión).

---

### 6. Clonar el Repositorio

```bash
# Ir al directorio home
cd ~

# Clonar el repositorio (reemplazá con tu URL)
git clone https://github.com/Brun02K20/ISW_2025_4K3_G12.git

# Navegar a la carpeta del backend
cd ISW_2025_4K3_G12/Entregas/Trabajos_Practicos/TP06_Test\ Driven\ Development\ \(TDD\)/Back
```

---

### 7. Verificar Archivos de Configuración

```bash
# Listar archivos del proyecto
ls -la

# Verificar que existan:
# - Dockerfile
# - docker-compose.yml
# - start_services.sh
# - requirements.txt
# - nginx.conf
```

```bash
# Ver contenido del docker-compose.yml (opcional)
cat docker-compose.yml
```

---

### 8. Preparar Scripts de Inicio

Si el repositorio fue clonado desde Windows, los archivos de texto pueden tener formato **CRLF** (Windows) en lugar de **LF** (Linux). Esto puede causar errores al ejecutar scripts.

```bash
# Instalar dos2unix
sudo apt install -y dos2unix

# Convertir start_services.sh a formato Linux (LF)
dos2unix start_services.sh

# Darle permisos de ejecución
chmod +x start_services.sh

# Verificar el formato (opcional)
file start_services.sh
# Debería mostrar: "ASCII text executable" o "... with LF line terminators"
```

---

### 9. Construir la Imagen Docker

```bash
# Construir la imagen del backend
docker compose build

# O usando docker build directamente:
docker build -t backend_app .
```

**Nota:** Este paso puede tardar varios minutos la primera vez, ya que descarga e instala todas las dependencias de Python.

---

### 10. Levantar los Servicios

#### Opción A: Levantar todos los servicios (incluye Nginx en puerto 80)

```bash
docker compose up -d
```

**⚠️ Advertencia:** Si ya tenés un servicio corriendo en el puerto 80 (como Apache, Nginx standalone, u otro contenedor), este comando fallará con error:

```
Error response from daemon: driver failed programming external connectivity on endpoint nginx_proxy: 
Bind for 0.0.0.0:80 failed: port is already allocated
```

**Solución:** Ver Opción B o Opción C abajo.

---

#### Opción B: Levantar solo PostgreSQL y Backend (sin Nginx)

Si no necesitás Nginx como reverse proxy, o ya tenés un servidor web corriendo en el puerto 80:

```bash
# Levanta solo postgres_db y backend_app
docker compose up -d postgres_db backend_app
```

El backend estará disponible en:
- **Puerto 8080** del servidor (acceso directo a FastAPI/Uvicorn)

Para probar desde tu PC:

```bash
curl http://tu-vps-ip:8080/
curl http://tu-vps-ip:8080/docs
```

---

#### Opción C: Cambiar el puerto de Nginx (modificar docker-compose.yml)

Si querés usar Nginx pero el puerto 80 está ocupado, podés mapear Nginx a otro puerto (ej: 8081):

1. Editar `docker-compose.yml`:

```yaml
  nginx_proxy:
    image: nginx:1.25-alpine
    container_name: nginx_proxy
    ports:
      - "8081:80"  # Cambiá "80:80" por "8081:80"
    # ... resto de la configuración
```

2. Levantar todos los servicios:

```bash
docker compose up -d
```

3. Acceder vía:

```bash
curl http://tu-vps-ip:8081/
```

---

### 11. Verificar el Estado de los Contenedores

```bash
# Ver contenedores en ejecución
docker ps

# Ver logs del backend
docker logs backend_app

# Ver logs de Postgres
docker logs postgres_db

# Ver logs de Nginx (si lo levantaste)
docker logs nginx_proxy

# Seguir los logs en tiempo real (Ctrl+C para salir)
docker logs -f backend_app
```

---

### 12. Configurar Firewall (UFW)

Si querés permitir tráfico HTTP/HTTPS y SSH:

```bash
# Habilitar UFW
sudo ufw enable

# Permitir SSH (puerto 22)
sudo ufw allow 22/tcp

# Permitir HTTP (puerto 80) — si usás Nginx en 80
sudo ufw allow 80/tcp

# Permitir HTTPS (puerto 443) — si configurás SSL
sudo ufw allow 443/tcp

# Permitir puerto 8080 (backend directo) — si no usás Nginx
sudo ufw allow 8080/tcp

# Ver estado del firewall
sudo ufw status
```

**Nota:** Si estás corriendo el backend en el puerto 8080 (sin Nginx), asegurate de abrir ese puerto en el firewall.

---

### 13. Probar la Aplicación

Desde tu PC local:

```bash
# Si levantaste Nginx en puerto 80:
curl http://tu-vps-ip/

# Si levantaste solo backend en 8080:
curl http://tu-vps-ip:8080/

# Acceder a la documentación interactiva (Swagger):
# En tu navegador:
http://tu-vps-ip:8080/docs
# o
http://tu-vps-ip/docs  # (si usás Nginx en puerto 80)
```

---

### 14. Verificar Base de Datos (Opcional)

```bash
# Conectarse al contenedor de Postgres
docker exec -it postgres_db psql -U postgres -d parque_db

# Dentro de psql, ejecutar:
\dt  # Listar tablas
\q   # Salir
```

---

## 🔄 Gestión de Contenedores

### Detener los servicios

```bash
docker compose down
```

### Reiniciar los servicios

```bash
docker compose restart
```

### Ver logs de un servicio específico

```bash
docker compose logs -f backend_app
docker compose logs -f postgres_db
docker compose logs -f nginx_proxy
```

### Reconstruir y levantar después de cambios en el código

```bash
# Detener contenedores
docker compose down

# Reconstruir imagen
docker compose build

# Levantar servicios
docker compose up -d
```

---

## 🛠️ Solución de Problemas

### Error: "port is already allocated" (puerto 80 u 8080 ocupado)

**Causa:** Otro servicio está usando el puerto.

**Solución 1:** Identificar y detener el servicio que usa el puerto:

```bash
# Ver qué proceso usa el puerto 80
sudo lsof -i :80

# Detener el servicio (ejemplo con Nginx standalone)
sudo systemctl stop nginx
sudo systemctl disable nginx

# O con Apache
sudo systemctl stop apache2
sudo systemctl disable apache2
```

**Solución 2:** Levantar solo `postgres_db` y `backend_app` (sin Nginx):

```bash
docker compose up -d postgres_db backend_app
```

**Solución 3:** Cambiar el mapeo de puerto en `docker-compose.yml` (ver Opción C arriba).

---

### Error: "bash: start_services.sh: /bin/sh^M: bad interpreter"

**Causa:** El archivo tiene terminaciones de línea de Windows (CRLF).

**Solución:**

```bash
sudo apt install -y dos2unix
dos2unix start_services.sh
chmod +x start_services.sh
docker compose build
```

---

### Error: "Cannot connect to the Docker daemon"

**Causa:** El servicio Docker no está corriendo o tu usuario no tiene permisos.

**Solución:**

```bash
# Iniciar Docker
sudo systemctl start docker

# Agregar tu usuario al grupo docker
sudo usermod -aG docker $USER

# Cerrar sesión y reconectarte por SSH
exit
ssh usuario@tu-vps-ip
```

---

### Error al construir la imagen: "ERROR [internal] load metadata for docker.io/library/python:3.12-slim"

**Causa:** Problemas de red o DNS al descargar la imagen base.

**Solución:**

```bash
# Verificar conectividad
ping -c 4 docker.io

# Reintentar la construcción
docker compose build --no-cache
```

---

## 📊 Puertos Usados

| Servicio      | Puerto Interno | Puerto Expuesto (Host) | Descripción                     |
|---------------|----------------|------------------------|---------------------------------|
| postgres_db   | 5432           | 5432                   | Base de datos PostgreSQL        |
| backend_app   | 8080           | 8080                   | API FastAPI (Uvicorn)           |
| nginx_proxy   | 80             | 80 (o 8081)            | Reverse proxy Nginx (opcional)  |

---

## 🔐 Variables de Entorno (Configuradas en docker-compose.yml)

| Variable         | Valor por defecto | Descripción                    |
|------------------|-------------------|--------------------------------|
| POSTGRES_USER    | postgres          | Usuario de PostgreSQL          |
| POSTGRES_PASSWORD| admin             | Contraseña de PostgreSQL       |
| POSTGRES_DB      | parque_db         | Nombre de la base de datos     |
| DB_HOST          | postgres_db       | Host de la base de datos       |
| DB_PORT          | 5432              | Puerto de la base de datos     |
| DB_USER          | postgres          | Usuario para conectar a la BD  |
| DB_PASSWORD      | admin             | Contraseña para conectar a BD  |
| DB_NAME          | parque_db         | Nombre de la BD en el backend  |

**⚠️ Importante:** Para producción, cambiá las credenciales por defecto (`admin`) por contraseñas seguras.

---

## 🔄 Actualizar la Aplicación (Nuevos Cambios del Repositorio)

```bash
# Ir al directorio del proyecto
cd ~/ISW_2025_4K3_G12/Entregas/Trabajos_Practicos/TP06_Test\ Driven\ Development\ \(TDD\)/Back

# Traer cambios del repositorio
git pull origin main  # o la rama que uses

# Convertir scripts si hay cambios
dos2unix start_services.sh

# Detener servicios
docker compose down

# Reconstruir imagen
docker compose build

# Levantar servicios
docker compose up -d

# Verificar logs
docker logs -f backend_app
```

---

## 📝 Notas Adicionales

- **Persistencia de datos:** Los datos de PostgreSQL se almacenan en un volumen Docker (`postgres_data`), por lo que no se pierden al reiniciar contenedores.
- **Logs:** Los logs de los contenedores se pueden ver con `docker logs <nombre_contenedor>`.
- **Producción:** Para un entorno de producción, considerá:
  - Usar variables de entorno seguras (archivo `.env`).
  - Configurar SSL/TLS con Let's Encrypt (Certbot).
  - Implementar backups automáticos de la base de datos.
  - Monitoreo con herramientas como Prometheus/Grafana.

---

## 📚 Referencias

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Uvicorn](https://www.uvicorn.org/)

---

## ✅ Resumen Rápido

```bash
# 1. Conectar al VPS
ssh usuario@tu-vps-ip

# 2. Actualizar sistema e instalar Docker
sudo apt update && sudo apt upgrade -y
# (Instalar Docker según Opción A o B arriba)

# 3. Configurar Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
exit  # Reconectar

# 4. Clonar repositorio
cd ~
git clone https://github.com/Brun02K20/ISW_2025_4K3_G12.git
cd ISW_2025_4K3_G12/Entregas/Trabajos_Practicos/TP06_Test\ Driven\ Development\ \(TDD\)/Back

# 5. Preparar scripts
sudo apt install -y dos2unix
dos2unix start_services.sh
chmod +x start_services.sh

# 6. Construir y levantar
docker compose build
docker compose up -d postgres_db backend_app  # Sin Nginx

# 7. Verificar
docker ps
docker logs backend_app
curl http://localhost:8080/

# 8. Configurar firewall (opcional)
sudo ufw allow 22/tcp
sudo ufw allow 8080/tcp
sudo ufw enable
```

---

**🎉 ¡Despliegue completado!** Tu aplicación debería estar corriendo en `http://tu-vps-ip:8080`.
