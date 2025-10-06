# 🧪 Guía de Testing y Validación

## ✅ Checklist de Verificación Rápida

### 1️⃣ Verificar Instalación

```powershell
# Backend
cd backend
python --version          # Debe ser 3.10+
pip list | findstr ultralytics
pip list | findstr fastapi

# Frontend
cd frontend
node --version           # Debe ser 18+
npm --version
```

---

### 2️⃣ Probar Backend (Solo)

```powershell
cd backend

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar servidor
python app.py
```

**Tests manuales:**

✅ **Health Check**
```powershell
# En otra terminal
curl http://localhost:8000/health
```
Respuesta esperada:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "gpu_available": false
}
```

✅ **API Docs**
- Abrir: http://localhost:8000/docs
- Debería ver Swagger UI con endpoints

✅ **Root Endpoint**
```powershell
curl http://localhost:8000/
```

✅ **Predict con imagen**
```powershell
curl -X POST "http://localhost:8000/predict" `
  -F "file=@C:\ruta\a\tu\imagen.jpg"
```

---

### 3️⃣ Probar Frontend (Solo)

```powershell
cd frontend
npm run dev
```

**Tests manuales:**

✅ **Verificar UI**
- Abrir: http://localhost:5173
- Debería ver la interfaz con dos tabs

✅ **Verificar conexión con backend**
- Si el backend NO está corriendo, debería ver errores en consola
- Abrir DevTools (F12) → Console

✅ **Probar subida de imagen**
1. Click en "Subir Imagen" tab
2. Seleccionar una imagen
3. Click en "Clasificar Billete"
4. Debería ver error si backend no está corriendo

---

### 4️⃣ Probar Full Stack

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

**Tests de integración:**

✅ **Test 1: Upload de Imagen**
1. Ir a http://localhost:5173
2. Tab "Subir Imagen"
3. Seleccionar imagen de billete
4. Click "Clasificar Billete"
5. ✅ Debería ver resultados con imagen anotada

✅ **Test 2: Cámara en Tiempo Real**
1. Tab "Cámara en Tiempo Real"
2. Click "Iniciar Cámara"
3. Permitir acceso a la cámara
4. Apuntar a un billete
5. ✅ Debería ver detecciones en vivo

✅ **Test 3: Verificar FPS**
- En modo cámara, verificar que FPS > 3
- Si FPS < 2, considerar optimización

---

### 5️⃣ Probar con Docker

```powershell
# Desde la raíz del proyecto
docker-compose up --build
```

**Esperar a que ambos servicios inicien (~2-3 minutos)**

✅ **Verificar servicios**
```powershell
docker-compose ps
```

Debería mostrar:
```
NAME                           STATUS
billetes-backend               Up (healthy)
billetes-frontend              Up
```

✅ **Acceder a la aplicación**
- Frontend: http://localhost
- Backend: http://localhost:8000/docs

---

### 6️⃣ Tests de Rendimiento

#### Medir tiempo de inferencia:

**Método 1: Desde API Docs**
1. Ir a http://localhost:8000/docs
2. POST /predict → Try it out
3. Subir imagen
4. Ver campo `inference_time` en respuesta

**Método 2: Desde logs**
```powershell
# En terminal del backend, ver logs
# Buscar líneas con tiempo de inferencia
```

**Benchmarks esperados:**
- CPU: 100-300ms por imagen
- GPU: 20-80ms por imagen

---

### 7️⃣ Test de Estrés (Opcional)

```powershell
# Instalar hey (HTTP load testing)
go install github.com/rakyll/hey@latest

# Test con 100 requests
hey -n 100 -c 10 -m POST `
  -D imagen.jpg `
  http://localhost:8000/predict
```

---

## 🐛 Troubleshooting Tests

### Backend no inicia

**Error: "ModuleNotFoundError: No module named 'fastapi'"**
```powershell
pip install -r requirements.txt
```

**Error: "Model file not found"**
```powershell
# Verificar que best.pt existe
ls backend\ml\best.pt

# Si no existe, copiar
copy ..\best.pt backend\ml\best.pt
```

**Error: "Port 8000 already in use"**
```powershell
# Matar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Frontend no conecta con Backend

**Error en consola: "Network Error"**
1. Verificar que backend esté corriendo
2. Verificar URL en `frontend/.env`:
   ```
   VITE_API_URL=http://localhost:8000
   ```
3. Reiniciar frontend después de cambiar .env

**Error: "CORS policy"**
1. Verificar `ALLOWED_ORIGINS` en backend
2. Debería incluir `http://localhost:5173`

---

### Cámara no funciona

**Error: "Permission denied"**
- Dar permisos de cámara en el navegador
- Configuración → Privacidad → Cámara

**Error: "WebSocket connection failed"**
1. Verificar backend esté corriendo
2. Verificar URL WebSocket en código
3. Usar `ws://` en local, `wss://` en producción

**Cámara negra/no muestra video**
- Verificar que no haya otra app usando la cámara
- Probar en otro navegador (Chrome recomendado)

---

### Docker no funciona

**Error: "Cannot connect to Docker daemon"**
```powershell
# Iniciar Docker Desktop
```

**Error: "Build failed"**
```powershell
# Ver logs específicos
docker-compose logs backend
docker-compose logs frontend
```

**Limpiar y reiniciar:**
```powershell
docker-compose down -v
docker-compose up --build --force-recreate
```

---

## 📊 Métricas de Éxito

### Backend:
- ✅ Health check responde en < 100ms
- ✅ Inferencia < 300ms (CPU) o < 100ms (GPU)
- ✅ WebSocket mantiene conexión estable
- ✅ Sin memory leaks después de 100 requests

### Frontend:
- ✅ Carga inicial < 2 segundos
- ✅ Upload de imagen funciona al primer intento
- ✅ Cámara muestra FPS > 3
- ✅ UI responsive en móvil

### Full Stack:
- ✅ End-to-end: upload → resultado < 2 segundos
- ✅ Streaming funciona sin lag visible
- ✅ Manejo de errores correcto (sin crashes)
- ✅ CORS configurado correctamente

---

## 🔧 Scripts de Testing Automatizado (Futuro)

```python
# backend/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict():
    with open("test_image.jpg", "rb") as f:
        response = client.post(
            "/predict",
            files={"file": f}
        )
    assert response.status_code == 200
    assert "detections" in response.json()
```

```bash
# Ejecutar tests
cd backend
pytest tests/
```

---

## 📝 Registro de Tests

| Fecha | Test | Resultado | Notas |
|-------|------|-----------|-------|
| 2025-10-05 | Backend Health | ✅ | 50ms response |
| 2025-10-05 | Predict Image | ✅ | 145ms inference |
| 2025-10-05 | Camera Stream | ✅ | 8 FPS |
| 2025-10-05 | Docker Build | ✅ | 3min build time |

---

**¡Feliz Testing! 🧪**
