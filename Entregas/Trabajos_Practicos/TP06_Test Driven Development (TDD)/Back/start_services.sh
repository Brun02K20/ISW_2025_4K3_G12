#!/bin/bash

# Script simple para levantar el servidor FastAPI
echo "� Levantando servidor FastAPI..."
echo "📍 API disponible en: http://localhost:8080"
echo "📖 Documentación en: http://localhost:8080/docs"
echo ""

while ! nc -z postgres_db 5432 -w1; do
  echo "⏳ Esperando a que la base de datos esté disponible..."
  sleep 1
done

# Ejecutar el servidor
alembic upgrade head
uvicorn src.application.main:app --host 0.0.0.0 --port 8080