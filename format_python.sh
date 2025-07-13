#!/bin/bash

# Script para formatear archivos Python automáticamente
# Uso: ./format_python.sh [archivo] o ./format_python.sh (para todos los archivos)

echo "🐍 Formateando archivos Python..."

# Activar el entorno virtual si existe
if [ -d "../.venv" ]; then
    source ../.venv/bin/activate
    echo "✅ Entorno virtual activado"
fi

# Si se proporciona un archivo específico
if [ $# -eq 1 ]; then
    echo "📝 Formateando archivo: $1"
    
    # Formatear con autopep8
    autopep8 --in-place --aggressive --aggressive "$1"
    
    # Organizar imports con isort
    isort "$1"
    
    echo "✅ Archivo $1 formateado correctamente"
else
    # Formatear todos los archivos .py
    echo "📝 Formateando todos los archivos Python..."
    
    for file in *.py; do
        if [ -f "$file" ]; then
            echo "  - Formateando: $file"
            autopep8 --in-place --aggressive --aggressive "$file"
            isort "$file"
        fi
    done
    
    echo "✅ Todos los archivos Python formateados correctamente"
fi

echo "🎉 ¡Formateo completado!"
echo "💡 Nota: Si tienes SQL dentro de strings multilinea, verifica la identación manualmente" 