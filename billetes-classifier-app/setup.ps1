# Script de instalacion y setup del proyecto
# Clasificador de Billetes Colombianos

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "Configurando Proyecto: Clasificador de Billetes Colombianos" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

# Variables
$PROJECT_ROOT = $PSScriptRoot
$BACKEND_DIR = Join-Path $PROJECT_ROOT "backend"
$FRONTEND_DIR = Join-Path $PROJECT_ROOT "frontend"

# Funcion para verificar comandos
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Verificar Python
Write-Host "[*] Verificando Python..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "[OK] $pythonVersion encontrado" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Python no encontrado. Por favor instala Python 3.10+" -ForegroundColor Red
    exit 1
}

# Verificar Node.js
Write-Host "[*] Verificando Node.js..." -ForegroundColor Yellow
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "[OK] Node.js $nodeVersion encontrado" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Node.js no encontrado. Por favor instala Node.js 18+" -ForegroundColor Red
    exit 1
}

Write-Host "`n----------------------------" -ForegroundColor Cyan
Write-Host "Configurando Backend..." -ForegroundColor Cyan
Write-Host "----------------------------`n" -ForegroundColor Cyan

# Setup Backend
Set-Location $BACKEND_DIR

# Crear entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "[*] Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "[OK] Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "[OK] Entorno virtual ya existe" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "[*] Activando entorno virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Instalar dependencias
Write-Host "[*] Instalando dependencias de Python..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Copiar .env
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "[OK] Archivo .env ya existe" -ForegroundColor Green
}

# Verificar modelo
$modelPath = Join-Path $BACKEND_DIR "ml\best.pt"
if (Test-Path $modelPath) {
    $modelSize = [math]::Round((Get-Item $modelPath).Length / 1MB, 2)
    Write-Host "[OK] Modelo YOLO encontrado ($modelSize MB)" -ForegroundColor Green
} else {
    Write-Host "[ADVERTENCIA] Modelo YOLO no encontrado en ml/best.pt" -ForegroundColor Yellow
    Write-Host "              Por favor copia tu archivo best.pt a: $modelPath" -ForegroundColor Yellow
}

Write-Host "`n----------------------------" -ForegroundColor Cyan
Write-Host "Configurando Frontend..." -ForegroundColor Cyan
Write-Host "----------------------------`n" -ForegroundColor Cyan

# Setup Frontend
Set-Location $FRONTEND_DIR

# Instalar dependencias
Write-Host "[*] Instalando dependencias de Node.js..." -ForegroundColor Yellow
npm install --silent

# Copiar .env
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "[OK] Archivo .env ya existe" -ForegroundColor Green
}

# Volver al directorio raiz
Set-Location $PROJECT_ROOT

Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "INSTALACION COMPLETADA CON EXITO!" -ForegroundColor Green
Write-Host "================================================================`n" -ForegroundColor Green
Write-Host "Proximos pasos:`n" -ForegroundColor Cyan
Write-Host "1. Iniciar Backend:" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python app.py`n" -ForegroundColor White
Write-Host "2. Iniciar Frontend (en otra terminal):" -ForegroundColor Yellow
Write-Host "   cd frontend" -ForegroundColor White
Write-Host "   npm run dev`n" -ForegroundColor White
Write-Host "3. Abrir navegador:" -ForegroundColor Yellow
Write-Host "   http://localhost:5173`n" -ForegroundColor White
Write-Host "Documentacion:" -ForegroundColor Cyan
Write-Host "   - README.md: Documentacion completa" -ForegroundColor White
Write-Host "   - QUICKSTART.md: Guia rapida" -ForegroundColor White
Write-Host "   - API Docs: http://localhost:8000/docs`n" -ForegroundColor White
Write-Host "Opcion con Docker:" -ForegroundColor Cyan
Write-Host "   docker-compose up --build`n" -ForegroundColor White
