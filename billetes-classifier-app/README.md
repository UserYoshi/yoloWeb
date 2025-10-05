# 💵 Clasificador de Billetes Colombianos

Aplicación web completa para clasificar billetes colombianos usando visión por computador con YOLO. Permite subir imágenes y usar la cámara en tiempo real.

![Stack](https://img.shields.io/badge/Stack-FastAPI%20%2B%20React-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Características

- ✅ **Clasificación de imágenes**: Sube fotos de billetes y obtén resultados instantáneos
- ✅ **Detección en tiempo real**: Usa tu cámara para clasificar billetes en vivo
- ✅ **Billetes detectados**: 1,000 | 2,000 | 5,000 | 10,000 | 20,000 | 50,000 | 100,000 COP
- ✅ **Cálculo automático**: Suma el valor total de todos los billetes detectados
- ✅ **Interfaz moderna**: UI responsive y amigable
- ✅ **API REST**: Backend con documentación automática (Swagger)
- ✅ **WebSocket**: Streaming de video en tiempo real

## 🏗️ Arquitectura

```
Frontend (React + Vite)  ←→  Backend (FastAPI)  ←→  YOLO Model
     Port 5173                  Port 8000              best.pt
```

### Stack Tecnológico

**Backend:**
- FastAPI (Python)
- Ultralytics YOLO
- OpenCV
- WebSocket
- PyTorch

**Frontend:**
- React 18
- Vite
- Axios
- CSS3 moderno

**Deployment:**
- Docker & Docker Compose
- Vercel (Frontend) / Railway (Backend)

## 📦 Estructura del Proyecto

```
billetes-classifier-app/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── predictor.py        # Lógica de predicción
│   ├── ml/
│   │   ├── best.pt             # 🔴 TU MODELO AQUÍ
│   │   └── README.md
│   ├── app.py                  # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.jsx     # Componente subir imagen
│   │   │   ├── ImageUpload.css
│   │   │   ├── CameraStream.jsx    # Componente cámara
│   │   │   └── CameraStream.css
│   │   ├── services/
│   │   │   └── api.js              # Cliente API
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.10+
- Node.js 18+
- npm o yarn
- (Opcional) Docker & Docker Compose

### 1️⃣ Clonar y Preparar

```bash
cd billetes-classifier-app

# Copiar tu modelo
copy ..\best.pt backend\ml\best.pt
```

### 2️⃣ Setup Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
copy .env.example .env

# Iniciar servidor
python app.py
```

El backend estará disponible en: `http://localhost:8000`
Documentación API: `http://localhost:8000/docs`

### 3️⃣ Setup Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Copiar variables de entorno
copy .env.example .env

# Iniciar desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

### 4️⃣ Opción con Docker (Más Fácil)

```bash
# Desde la raíz del proyecto
docker-compose up --build

# Acceder:
# Frontend: http://localhost
# Backend: http://localhost:8000
```

## 📖 Uso de la API

### Endpoint: Predecir Imagen

```bash
POST http://localhost:8000/predict
Content-Type: multipart/form-data

# Ejemplo con curl
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@billete.jpg"
```

**Respuesta:**
```json
{
  "success": true,
  "detections": [
    {
      "class": "50000",
      "confidence": 95.32,
      "is_colombian": true,
      "message": "Billete colombiano de $50000 COP"
    }
  ],
  "total_detected": 1,
  "total_value": 50000,
  "inference_time": 145.23,
  "annotated_image": "data:image/jpeg;base64,..."
}
```

### WebSocket: Streaming en Tiempo Real

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/predict')

ws.onopen = () => {
  // Enviar frame (base64)
  ws.send(frameBase64)
}

ws.onmessage = (event) => {
  const result = JSON.parse(event.data)
  console.log(result.detections)
}
```

## 🌐 Despliegue en Producción

### Opción 1: Vercel (Frontend) + Railway (Backend)

#### Backend en Railway

1. Crear cuenta en [Railway.app](https://railway.app)
2. Conectar repositorio o deployar desde CLI
3. Agregar variables de entorno
4. Railway detectará automáticamente el Dockerfile
5. Copiar URL generada

#### Frontend en Vercel

1. Crear cuenta en [Vercel.com](https://vercel.com)
2. Importar repositorio (carpeta `frontend/`)
3. Configurar variable de entorno:
   ```
   VITE_API_URL=https://tu-backend.railway.app
   ```
4. Deploy automático

### Opción 2: Render (Backend + Frontend)

1. Crear cuenta en [Render.com](https://render.com)
2. Crear Web Service para backend (Dockerfile)
3. Crear Static Site para frontend
4. Configurar variables de entorno

### Opción 3: AWS/GCP/Azure

Ver documentación específica de cada proveedor para Docker deployments.

## 🔧 Configuración

### Variables de Entorno

**Backend (`.env`):**
```env
PORT=8000
HOST=0.0.0.0
DEBUG=False
MODEL_PATH=ml/best.pt
ALLOWED_ORIGINS=https://tu-frontend.vercel.app
```

**Frontend (`.env`):**
```env
VITE_API_URL=https://tu-backend.railway.app
```

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

## 📊 Rendimiento

- **Inferencia**: ~100-200ms por imagen (CPU)
- **Streaming**: ~5-10 FPS (depende del hardware)
- **GPU**: Acelera inferencia 3-5x

## 🐛 Troubleshooting

### Error: "No se pudo cargar el modelo"
- Verifica que `best.pt` esté en `backend/ml/`
- Verifica la versión de ultralytics

### Error: "CORS policy"
- Agrega tu dominio frontend a `ALLOWED_ORIGINS` en backend

### Error: "WebSocket connection failed"
- Verifica que el backend esté corriendo
- Revisa la URL del WebSocket (ws:// no wss://)

### Cámara no funciona
- Usa HTTPS en producción (requerido por navegadores)
- Verifica permisos de cámara en el navegador

## 📝 Próximas Mejoras

- [ ] Historial de clasificaciones (con BD)
- [ ] Autenticación de usuarios
- [ ] Exportar reportes PDF
- [ ] Soporte para múltiples monedas
- [ ] Modelo optimizado con ONNX
- [ ] Progressive Web App (PWA)
- [ ] Analytics dashboard

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - ve [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Desarrollado con ❤️ usando FastAPI + React + YOLO

## 🙏 Agradecimientos

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)

---

⭐ Si te gustó este proyecto, ¡dale una estrella en GitHub!
