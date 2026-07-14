#!/bin/bash
# Script de inicio robusto

# Detectar comando Python disponible
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ No se encontró Python"
    exit 1
fi

echo "🐍 Usando: $PYTHON_CMD"

# Usar gunicorn si está disponible, sino Python directo
if command -v gunicorn &> /dev/null; then
    echo "🚀 Iniciando con gunicorn..."
    gunicorn servidor_todo_en_uno:app --bind 0.0.0.0:${PORT:-8080}
else
    echo "🚀 Iniciando con Python directo..."
    $PYTHON_CMD servidor_todo_en_uno.py
fi
