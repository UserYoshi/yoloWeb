"""
FastAPI Backend para Clasificación de Billetes Colombianos
"""
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import cv2
import numpy as np
from api.predictor import BilletePredictor
import base64
import json

app = FastAPI(
    title="Clasificador de Billetes API",
    description="API para clasificar billetes colombianos usando YOLO",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar predictor (carga el modelo una sola vez)
predictor = None


@app.on_event("startup")
async def startup_event():
    """Cargar modelo al iniciar la aplicación"""
    global predictor
    print("🚀 Iniciando servidor...")
    print("📦 Cargando modelo YOLO...")
    predictor = BilletePredictor(model_path="ml/best.pt")
    print("✅ Modelo cargado exitosamente!")


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de Clasificación de Billetes Colombianos 💵",
        "status": "online",
        "endpoints": {
            "predict_image": "/predict",
            "health": "/health",
            "websocket": "/ws/predict"
        }
    }


@app.get("/health")
async def health_check():
    """Verificar estado del servidor y modelo"""
    return {
        "status": "healthy",
        "model_loaded": predictor is not None,
        "gpu_available": predictor.gpu_available if predictor else False
    }


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Clasificar una imagen de billete subida por el usuario
    
    Args:
        file: Imagen en formato jpg, png, etc.
    
    Returns:
        JSON con predicciones y billetes detectados
    """
    try:
        # Leer imagen
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return JSONResponse(
                status_code=400,
                content={"error": "No se pudo leer la imagen"}
            )
        
        # Hacer predicción
        results = predictor.predict(image)
        
        # Codificar imagen anotada a base64
        _, buffer = cv2.imencode('.jpg', results['annotated_image'])
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "success": True,
            "detections": results['detections'],
            "total_detected": results['total_detected'],
            "total_value": results['total_value'],
            "inference_time": results['inference_time'],
            "annotated_image": f"data:image/jpeg;base64,{img_base64}"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error en predicción: {str(e)}"}
        )


@app.websocket("/ws/predict")
async def websocket_predict(websocket: WebSocket):
    """
    WebSocket para streaming de video en tiempo real
    Recibe frames de la cámara y devuelve predicciones
    """
    await websocket.accept()
    print("🔌 Cliente conectado al WebSocket")
    
    try:
        while True:
            # Recibir frame como base64
            data = await websocket.receive_text()
            
            # Decodificar imagen
            img_data = base64.b64decode(data.split(',')[1] if ',' in data else data)
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                await websocket.send_json({
                    "error": "Frame inválido"
                })
                continue
            
            # Hacer predicción
            results = predictor.predict(frame)
            
            # Codificar imagen anotada
            _, buffer = cv2.imencode('.jpg', results['annotated_image'])
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Enviar resultados
            await websocket.send_json({
                "success": True,
                "detections": results['detections'],
                "total_detected": results['total_detected'],
                "total_value": results['total_value'],
                "fps": results.get('fps', 0),
                "annotated_image": f"data:image/jpeg;base64,{img_base64}"
            })
            
    except WebSocketDisconnect:
        print("🔌 Cliente desconectado del WebSocket")
    except Exception as e:
        print(f"❌ Error en WebSocket: {e}")
        await websocket.close()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Solo para desarrollo
    )
