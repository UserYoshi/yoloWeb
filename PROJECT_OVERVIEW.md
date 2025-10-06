# 📁 Estructura del Proyecto Generado

```
billetes-classifier-app/
│
├── 📄 README.md                    # Documentación principal completa
├── 📄 QUICKSTART.md                # Guía rápida de inicio (5 minutos)
├── 📄 DEPLOYMENT.md                # Guía detallada de deployment
├── 📄 STRUCTURE.txt                # Este archivo - estructura del proyecto
├── 🐳 docker-compose.yml           # Orquestación Docker
├── 🔧 setup.ps1                    # Script de instalación (Windows)
└── 🔧 setup.sh                     # Script de instalación (Linux/Mac)
│
├── 🔙 backend/                     # ===== BACKEND (FastAPI + YOLO) =====
│   │
│   ├── 📄 app.py                   # ⭐ Aplicación principal FastAPI
│   ├── 📄 requirements.txt         # Dependencias Python
│   ├── 📄 Dockerfile               # Containerización backend
│   ├── 📄 .env.example             # Template variables de entorno
│   ├── 📄 .gitignore              # Archivos ignorados por Git
│   │
│   ├── 📂 api/                     # Módulos API
│   │   ├── __init__.py
│   │   └── 📄 predictor.py         # ⭐ Lógica de predicción YOLO
│   │
│   └── 📂 ml/                      # Modelos de Machine Learning
│       ├── 📄 README.md
│       └── 🧠 best.pt              # ⭐⭐⭐ TU MODELO YOLO (copiar aquí)
│
└── 🎨 frontend/                    # ===== FRONTEND (React + Vite) =====
    │
    ├── 📄 package.json             # Dependencias Node.js
    ├── 📄 vite.config.js           # Configuración Vite
    ├── 📄 index.html               # HTML principal
    ├── 📄 Dockerfile               # Containerización frontend
    ├── 📄 nginx.conf               # Configuración Nginx (producción)
    ├── 📄 .env.example             # Template variables de entorno
    ├── 📄 .gitignore              # Archivos ignorados por Git
    │
    ├── 📂 public/                  # Archivos estáticos públicos
    │
    └── 📂 src/                     # ===== CÓDIGO FUENTE =====
        │
        ├── 📄 main.jsx             # Entry point React
        ├── 📄 App.jsx              # ⭐ Componente principal
        ├── 📄 App.css              # Estilos App
        ├── 📄 index.css            # Estilos globales
        │
        ├── 📂 components/          # Componentes React
        │   │
        │   ├── 📄 ImageUpload.jsx  # ⭐ Componente subir imagen
        │   ├── 📄 ImageUpload.css  # Estilos ImageUpload
        │   ├── 📄 CameraStream.jsx # ⭐ Componente cámara tiempo real
        │   └── 📄 CameraStream.css # Estilos CameraStream
        │
        └── 📂 services/            # Servicios/API clients
            └── 📄 api.js           # ⭐ Cliente HTTP para backend
```

---

## 🎯 Archivos Clave

### Backend (Python/FastAPI):
1. **`backend/app.py`** - Servidor FastAPI con endpoints REST y WebSocket
2. **`backend/api/predictor.py`** - Clase que maneja la inferencia YOLO
3. **`backend/ml/best.pt`** - 🔴 **¡IMPORTANTE!** Tu modelo entrenado va aquí

### Frontend (React):
1. **`frontend/src/App.jsx`** - Componente raíz con tabs
2. **`frontend/src/components/ImageUpload.jsx`** - UI para subir imágenes
3. **`frontend/src/components/CameraStream.jsx`** - UI para cámara en tiempo real
4. **`frontend/src/services/api.js`** - Cliente HTTP para llamar al backend

### Configuración:
1. **`docker-compose.yml`** - Orquestación de contenedores
2. **`backend/Dockerfile`** - Imagen Docker del backend
3. **`frontend/Dockerfile`** - Imagen Docker del frontend
4. **`.env.example`** - Templates de variables de entorno

### Documentación:
1. **`README.md`** - Documentación completa (este archivo)
2. **`QUICKSTART.md`** - Inicio rápido para desarrolladores
3. **`DEPLOYMENT.md`** - Guía de deployment en producción

---

## 🔢 Estadísticas del Proyecto

- **Total archivos**: ~35
- **Lenguajes**: Python (Backend), JavaScript/JSX (Frontend)
- **Frameworks**: FastAPI, React, Vite
- **Líneas de código**: ~2,500+
- **Componentes React**: 2 principales
- **Endpoints API**: 4 (/, /health, /predict, /ws/predict)

---

## 🚀 Flujo de Datos

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       ▼
┌────────────────────────────────┐
│  FRONTEND (React)              │
│  - ImageUpload Component       │
│  - CameraStream Component      │
└────────┬───────────────────────┘
         │ HTTP POST / WebSocket
         ▼
┌────────────────────────────────┐
│  BACKEND (FastAPI)             │
│  - /predict endpoint           │
│  - /ws/predict WebSocket       │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  YOLO Predictor                │
│  - Carga best.pt               │
│  - Procesa imagen              │
│  - Detecta billetes            │
│  - Anota imagen                │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Respuesta JSON                │
│  - Detecciones                 │
│  - Imagen anotada (base64)     │
│  - Confianza, valor total      │
└────────────────────────────────┘
```

---

## 📦 Dependencias Principales

### Backend:
```
fastapi          - Framework web
uvicorn          - Servidor ASGI
ultralytics      - YOLO
opencv-python    - Procesamiento de imágenes
torch            - PyTorch (deep learning)
websockets       - WebSocket support
```

### Frontend:
```
react            - UI library
axios            - HTTP client
vite             - Build tool
```

---

## 🎨 Características Implementadas

✅ **Clasificación por imagen**
- Upload de archivos
- Preview de imagen
- Resultados con confianza
- Valor total calculado

✅ **Clasificación en tiempo real**
- Acceso a cámara web
- Streaming via WebSocket
- FPS display
- Detecciones en vivo

✅ **Backend robusto**
- API REST documentada (Swagger)
- WebSocket para streaming
- Manejo de errores
- Health check endpoint

✅ **Frontend moderno**
- UI responsive
- Animaciones suaves
- Manejo de estados
- Error handling

✅ **Deployment ready**
- Dockerfiles
- Docker Compose
- Configuración para Railway/Vercel
- Scripts de instalación

---

## 📝 Próximos Pasos Sugeridos

1. ✅ **Copiar `best.pt` a `backend/ml/`**
2. ✅ **Ejecutar `setup.ps1` o `setup.sh`**
3. ✅ **Iniciar backend y frontend**
4. ✅ **Probar localmente**
5. ⬜ **Deployar en producción** (ver DEPLOYMENT.md)
6. ⬜ **Agregar features adicionales** (historial, users, etc.)

---

## 🤝 Contribuciones Futuras

Ideas para expandir el proyecto:
- [ ] Base de datos para historial
- [ ] Autenticación de usuarios
- [ ] Dashboard de analytics
- [ ] Soporte múltiples monedas
- [ ] API rate limiting
- [ ] Tests unitarios
- [ ] CI/CD pipeline
- [ ] Progressive Web App (PWA)

---

**Generado con ❤️ para clasificación de billetes colombianos 💵**
