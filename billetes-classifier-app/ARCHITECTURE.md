# 🏗️ Arquitectura del Sistema

## Vista General del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO FINAL                           │
│                  (Navegador Web / Móvil)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                      │
│                     Puerto 5173 (dev) / 80 (prod)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐      ┌──────────────────────┐       │
│  │  ImageUpload         │      │  CameraStream        │       │
│  │  Component           │      │  Component           │       │
│  │                      │      │                      │       │
│  │  - File Upload       │      │  - Camera Access     │       │
│  │  - Preview           │      │  - WebSocket Stream  │       │
│  │  - HTTP POST         │      │  - Live Detection    │       │
│  └──────────────────────┘      └──────────────────────┘       │
│              │                              │                   │
│              │                              │                   │
│  ┌───────────▼──────────────────────────────▼───────────────┐  │
│  │           API Service (axios)                            │  │
│  │           - HTTP Client                                  │  │
│  │           - WebSocket Client                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              │ HTTP REST                   │ WebSocket
              │ (POST /predict)             │ (ws://host/ws/predict)
              │                             │
              ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│                    Puerto 8000                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                         │  │
│  │                                                          │  │
│  │  GET  /              → Info general                     │  │
│  │  GET  /health        → Health check                     │  │
│  │  POST /predict       → Clasificar imagen               │  │
│  │  WS   /ws/predict    → Streaming en tiempo real        │  │
│  │                                                          │  │
│  └────────────┬─────────────────────────────┬──────────────┘  │
│               │                             │                  │
│               ▼                             ▼                  │
│  ┌────────────────────────┐   ┌──────────────────────────┐    │
│  │  HTTP Handler          │   │  WebSocket Handler       │    │
│  │  - Recibe imagen       │   │  - Recibe frames         │    │
│  │  - Valida formato      │   │  - Stream continuo       │    │
│  │  - Llama predictor     │   │  - Llama predictor       │    │
│  │  - Retorna JSON        │   │  - Retorna JSON stream   │    │
│  └────────────┬───────────┘   └──────────────┬───────────┘    │
│               │                              │                 │
│               └──────────────┬───────────────┘                 │
│                              │                                 │
│                              ▼                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              BilletePredictor                            │ │
│  │              (api/predictor.py)                          │ │
│  │                                                          │ │
│  │  - Carga modelo YOLO al inicio (startup)                │ │
│  │  - Preprocesa imágenes                                  │ │
│  │  - Ejecuta inferencia                                   │ │
│  │  - Postprocesa resultados                               │ │
│  │  - Anota imágenes con detecciones                       │ │
│  │  - Calcula valor total                                  │ │
│  │                                                          │ │
│  └────────────────────────┬─────────────────────────────────┘ │
│                           │                                    │
│                           ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              YOLO Model (best.pt)                        │ │
│  │              ml/best.pt                                  │ │
│  │                                                          │ │
│  │  - Cargado en RAM/VRAM una sola vez                     │ │
│  │  - Detección de objetos (billetes)                      │ │
│  │  - Clasificación de denominación                        │ │
│  │  - Cálculo de confianza                                 │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Datos Detallado

### 1️⃣ Flujo: Upload de Imagen

```
┌─────────┐
│ Usuario │
└────┬────┘
     │ 1. Selecciona imagen
     ▼
┌──────────────┐
│ ImageUpload  │
│ Component    │
└────┬─────────┘
     │ 2. Crea FormData
     │    file: File
     ▼
┌──────────────┐
│ API Service  │
│ (axios)      │
└────┬─────────┘
     │ 3. HTTP POST /predict
     │    Content-Type: multipart/form-data
     ▼
┌──────────────┐
│ FastAPI      │
│ POST Handler │
└────┬─────────┘
     │ 4. await file.read()
     │    cv2.imdecode()
     ▼
┌──────────────┐
│ Predictor    │
│ .predict()   │
└────┬─────────┘
     │ 5. YOLO inference
     │    results = model(image)
     ▼
┌──────────────┐
│ YOLO Model   │
│ (best.pt)    │
└────┬─────────┘
     │ 6. Detecciones
     │    boxes, classes, confidence
     ▼
┌──────────────┐
│ Predictor    │
│ postprocess  │
└────┬─────────┘
     │ 7. Anota imagen
     │    Calcula total
     │    Crea JSON response
     ▼
┌──────────────┐
│ FastAPI      │
│ Response     │
└────┬─────────┘
     │ 8. JSON + base64 image
     │    {
     │      detections: [...],
     │      total_value: 50000,
     │      annotated_image: "data:image..."
     │    }
     ▼
┌──────────────┐
│ ImageUpload  │
│ Component    │
└────┬─────────┘
     │ 9. Muestra resultado
     ▼
┌─────────┐
│ Usuario │
│ ve      │
│ resultado│
└─────────┘
```

**Tiempo total**: ~100-300ms (CPU) | ~20-80ms (GPU)

---

### 2️⃣ Flujo: Streaming de Cámara

```
┌─────────┐
│ Usuario │
└────┬────┘
     │ 1. Click "Iniciar Cámara"
     ▼
┌──────────────┐
│CameraStream  │
│Component     │
└────┬─────────┘
     │ 2. navigator.mediaDevices
     │    .getUserMedia()
     ▼
┌──────────────┐
│ Navegador    │
│ pide permiso │
└────┬─────────┘
     │ 3. Usuario acepta
     │    Stream activado
     ▼
┌──────────────┐
│CameraStream  │
│videoRef      │
└────┬─────────┘
     │ 4. Conectar WebSocket
     │    ws://host:8000/ws/predict
     ▼
┌──────────────┐
│ WebSocket    │
│ Connection   │
└────┬─────────┘
     │ 5. ws.onopen
     │    Conexión establecida
     ▼
┌──────────────┐
│CameraStream  │
│Loop (200ms)  │
└────┬─────────┘
     │ 6. Captura frame
     │    canvas.toBlob()
     │    reader.readAsDataURL()
     ▼
┌──────────────┐
│ WebSocket    │
│ ws.send()    │
└────┬─────────┘
     │ 7. Frame base64 →
     ▼
┌──────────────┐
│ FastAPI      │
│ WS Handler   │
└────┬─────────┘
     │ 8. await ws.receive_text()
     │    base64.decode()
     │    cv2.imdecode()
     ▼
┌──────────────┐
│ Predictor    │
│ .predict()   │
└────┬─────────┘
     │ 9. YOLO inference
     ▼
┌──────────────┐
│ YOLO Model   │
└────┬─────────┘
     │ 10. Detecciones
     ▼
┌──────────────┐
│ FastAPI      │
│ WS Handler   │
└────┬─────────┘
     │ 11. ws.send_json()
     │     {
     │       detections: [...],
     │       annotated_image: "...",
     │       fps: 8.5
     │     }
     ▼
┌──────────────┐
│CameraStream  │
│ws.onmessage  │
└────┬─────────┘
     │ 12. Actualiza estado
     │     setResult(data)
     ▼
┌─────────┐
│ Usuario │
│ ve      │
│ stream  │
│ en vivo │
└─────────┘
     ▲
     │ Loop continuo cada 200ms
     └─────────────────────────
```

**FPS**: 3-8 (CPU) | 10-30 (GPU)
**Latencia**: ~200-500ms end-to-end

---

## Componentes y Responsabilidades

### Frontend (React)

```
src/
├── main.jsx                 # Entry point
│   └── monta App.jsx
│
├── App.jsx                  # Componente raíz
│   ├── Maneja tabs
│   ├── Estado global (activeTab)
│   └── Renderiza:
│       ├── ImageUpload (si tab=upload)
│       └── CameraStream (si tab=camera)
│
├── components/
│   ├── ImageUpload.jsx      # Subida de imagen
│   │   ├── Estados: file, preview, result
│   │   ├── handleFileSelect()
│   │   ├── handleUpload() → API
│   │   └── Renderiza resultados
│   │
│   └── CameraStream.jsx     # Streaming cámara
│       ├── Estados: isStreaming, result
│       ├── startStreaming() → WebSocket
│       ├── captureAndSendFrame()
│       └── Renderiza video + overlay
│
└── services/
    └── api.js               # Cliente HTTP
        ├── axios instance
        ├── predictImage(file)
        └── checkHealth()
```

### Backend (FastAPI)

```
backend/
├── app.py                   # FastAPI app
│   ├── startup_event()      # Carga modelo
│   ├── GET  /               # Info
│   ├── GET  /health         # Health check
│   ├── POST /predict        # Clasificar imagen
│   └── WS   /ws/predict     # Streaming
│
├── api/
│   └── predictor.py         # Lógica ML
│       └── BilletePredictor
│           ├── __init__()        # Carga YOLO
│           ├── predict(image)    # Inferencia
│           ├── _get_message()    # Genera texto
│           └── _annotate_image() # Dibuja boxes
│
└── ml/
    └── best.pt              # Modelo YOLO
```

---

## Tecnologías por Capa

### 🎨 Capa de Presentación (Frontend)
```
┌─────────────────────────────────────┐
│ React 18                            │
│ - Componentes funcionales           │
│ - Hooks (useState, useRef, etc)     │
│ - JSX                               │
├─────────────────────────────────────┤
│ Vite                                │
│ - Build tool moderno                │
│ - Hot Module Replacement (HMR)      │
│ - Optimización automática           │
├─────────────────────────────────────┤
│ Axios                               │
│ - HTTP client                       │
│ - Interceptors                      │
│ - Form data handling                │
├─────────────────────────────────────┤
│ CSS3                                │
│ - Flexbox / Grid                    │
│ - Animations                        │
│ - Media queries (responsive)        │
├─────────────────────────────────────┤
│ WebSocket API (native)              │
│ - Real-time communication           │
│ - Binary/Text messages              │
└─────────────────────────────────────┘
```

### ⚙️ Capa de Aplicación (Backend)
```
┌─────────────────────────────────────┐
│ FastAPI                             │
│ - Async endpoints                   │
│ - Automatic validation (Pydantic)   │
│ - OpenAPI/Swagger docs              │
│ - WebSocket support                 │
├─────────────────────────────────────┤
│ Uvicorn                             │
│ - ASGI server                       │
│ - WebSocket support                 │
│ - Production-ready                  │
├─────────────────────────────────────┤
│ Python 3.10+                        │
│ - Type hints                        │
│ - Async/await                       │
│ - Modern features                   │
└─────────────────────────────────────┘
```

### 🧠 Capa de ML (Modelo)
```
┌─────────────────────────────────────┐
│ Ultralytics YOLOv8                  │
│ - Object detection                  │
│ - Classification                    │
│ - Custom trained (best.pt)          │
├─────────────────────────────────────┤
│ PyTorch                             │
│ - Deep learning framework           │
│ - GPU acceleration (CUDA)           │
│ - Model loading/inference           │
├─────────────────────────────────────┤
│ OpenCV (cv2)                        │
│ - Image processing                  │
│ - Drawing annotations               │
│ - Format conversions                │
├─────────────────────────────────────┤
│ NumPy                               │
│ - Array operations                  │
│ - Image as arrays                   │
└─────────────────────────────────────┘
```

### 🐳 Capa de Infraestructura
```
┌─────────────────────────────────────┐
│ Docker                              │
│ - Containerización                  │
│ - Aislamiento de dependencias       │
│ - Portabilidad                      │
├─────────────────────────────────────┤
│ Docker Compose                      │
│ - Multi-container orchestration     │
│ - Network configuration             │
│ - Volume management                 │
├─────────────────────────────────────┤
│ Nginx (producción)                  │
│ - Reverse proxy                     │
│ - Static file serving               │
│ - Load balancing                    │
└─────────────────────────────────────┘
```

---

## Escalabilidad y Optimizaciones

### Actuales:
- ✅ Modelo cargado una sola vez (no por request)
- ✅ Async/await en backend
- ✅ WebSocket para reducir overhead HTTP
- ✅ Imágenes en base64 (no almacenadas)
- ✅ CORS configurado

### Futuras Mejoras:
- [ ] Redis para caché de resultados
- [ ] Load balancer (múltiples instancias backend)
- [ ] CDN para frontend
- [ ] Modelo optimizado con ONNX
- [ ] Batch processing para múltiples imágenes
- [ ] Queue system (Celery) para requests pesados

---

**Arquitectura diseñada para**: Escalabilidad | Mantenibilidad | Performance
