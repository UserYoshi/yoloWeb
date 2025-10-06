#!/bin/bash
# Script de instalación para Linux/Mac
# Clasificador de Billetes Colombianos

echo "💵 Configurando Proyecto: Clasificador de Billetes Colombianos"
echo "================================================================"
echo ""

PROJECT_ROOT=$(cd "$(dirname "$0")" && pwd)
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# Verificar Python
echo "🔍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION encontrado"
else
    echo "❌ Python no encontrado. Por favor instala Python 3.10+"
    exit 1
fi

# Verificar Node.js
echo "🔍 Verificando Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js $NODE_VERSION encontrado"
else
    echo "❌ Node.js no encontrado. Por favor instala Node.js 18+"
    exit 1
fi

echo ""
echo "📦 Configurando Backend..."
echo "----------------------------"

# Setup Backend
cd "$BACKEND_DIR"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "🔨 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "⚡ Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias de Python..."
pip install -r requirements.txt -q

# Copiar .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Archivo .env creado"
else
    echo "✅ Archivo .env ya existe"
fi

# Verificar modelo
MODEL_PATH="$BACKEND_DIR/ml/best.pt"
if [ -f "$MODEL_PATH" ]; then
    MODEL_SIZE=$(du -h "$MODEL_PATH" | cut -f1)
    echo "✅ Modelo YOLO encontrado ($MODEL_SIZE)"
else
    echo "⚠️  Modelo YOLO no encontrado en ml/best.pt"
    echo "   Por favor copia tu archivo best.pt a: $MODEL_PATH"
fi

echo ""
echo "⚛️  Configurando Frontend..."
echo "----------------------------"

# Setup Frontend
cd "$FRONTEND_DIR"

# Instalar dependencias
echo "📥 Instalando dependencias de Node.js..."
npm install --silent

# Copiar .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Archivo .env creado"
else
    echo "✅ Archivo .env ya existe"
fi

# Volver al directorio raíz
cd "$PROJECT_ROOT"

echo ""
echo "================================================================"
echo "✅ ¡Instalación completada con éxito!"
echo "================================================================"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1️⃣  Iniciar Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "2️⃣  Iniciar Frontend (en otra terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3️⃣  Abrir navegador:"
echo "   http://localhost:5173"
echo ""
echo "📚 Documentación:"
echo "   - README.md: Documentación completa"
echo "   - QUICKSTART.md: Guía rápida"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "🐳 Opción con Docker:"
echo "   docker-compose up --build"
echo ""
