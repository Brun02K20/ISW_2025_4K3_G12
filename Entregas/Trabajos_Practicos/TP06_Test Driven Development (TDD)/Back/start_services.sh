#!/bin/bash

# Script simple para levantar el servidor FastAPI
echo "� Levantando servidor FastAPI..."
echo "📍 API disponible en: http://localhost:8080"
echo "📖 Documentación en: http://localhost:8080/docs"
echo ""

# Ejecutar el servidor
uvicorn src.application.main:app --host 0.0.0.0 --port 8080 --reload