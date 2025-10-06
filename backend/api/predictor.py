"""
Módulo de predicción para clasificación de billetes colombianos
"""
from ultralytics import YOLO
import cv2
import torch
import time
from typing import Dict, List, Any


class BilletePredictor:
    """Clase para manejar predicciones de billetes colombianos"""
    
    # Denominaciones válidas de billetes colombianos
    BILLETES_COLOMBIANOS = {
        "1000", "2000", "5000", "10000", "20000", "50000", "100000"
    }
    
    # Colores para cada denominación (BGR)
    COLORES = {
        "1000": (255, 0, 0),      # Azul
        "2000": (255, 0, 255),    # Magenta
        "5000": (0, 255, 255),    # Amarillo
        "10000": (0, 255, 0),     # Verde
        "20000": (0, 165, 255),   # Naranja
        "50000": (128, 0, 128),   # Morado
        "100000": (0, 0, 255)     # Rojo
    }
    
    def __init__(self, model_path: str = "ml/best.pt"):
        """
        Inicializar el predictor
        
        Args:
            model_path: Ruta al modelo YOLO entrenado
        """
        print(f"📦 Cargando modelo desde: {model_path}")
        self.model = YOLO(model_path)
        self.gpu_available = torch.cuda.is_available()
        
        if self.gpu_available:
            print("✅ GPU disponible - Usando aceleración CUDA")
        else:
            print("⚠️  GPU no disponible - Usando CPU")
    
    def predict(self, image) -> Dict[str, Any]:
        """
        Realizar predicción sobre una imagen
        
        Args:
            image: Imagen en formato numpy array (OpenCV)
        
        Returns:
            Diccionario con resultados de la predicción
        """
        start_time = time.time()
        
        # Realizar inferencia
        results = self.model(image, verbose=False)
        
        # Procesar detecciones
        detections = []
        total_value = 0
        
        for box in results[0].boxes:
            clase_idx = int(box.cls[0])
            clase_nombre = results[0].names[clase_idx]
            confidence = float(box.conf[0])
            
            # Verificar si es billete colombiano
            is_colombian = clase_nombre in self.BILLETES_COLOMBIANOS
            
            detection = {
                "class": clase_nombre,
                "confidence": round(confidence * 100, 2),
                "is_colombian": is_colombian,
                "message": self._get_message(clase_nombre, is_colombian)
            }
            
            detections.append(detection)
            
            # Sumar valor total si es billete colombiano
            if is_colombian:
                try:
                    total_value += int(clase_nombre)
                except ValueError:
                    pass
        
        # Obtener imagen anotada
        annotated_image = self._annotate_image(image, results[0], detections)
        
        inference_time = time.time() - start_time
        fps = 1 / inference_time if inference_time > 0 else 0
        
        return {
            "detections": detections,
            "total_detected": len(detections),
            "total_value": total_value,
            "inference_time": round(inference_time * 1000, 2),  # ms
            "fps": round(fps, 2),
            "annotated_image": annotated_image
        }
    
    def _get_message(self, clase_nombre: str, is_colombian: bool) -> str:
        """Generar mensaje descriptivo para la detección"""
        if is_colombian:
            return f"Billete colombiano de ${clase_nombre} COP"
        else:
            return f"Billete no colombiano o desconocido: {clase_nombre}"
    
    def _annotate_image(self, image, result, detections: List[Dict]) -> Any:
        """
        Anotar imagen con detecciones y colores personalizados
        
        Args:
            image: Imagen original
            result: Resultado de YOLO
            detections: Lista de detecciones procesadas
        
        Returns:
            Imagen anotada
        """
        # Obtener imagen anotada por YOLO
        annotated = result.plot()
        
        # Agregar información adicional
        y_offset = 30
        for i, det in enumerate(detections):
            text = f"{det['message']} ({det['confidence']}%)"
            color = self.COLORES.get(det['class'], (255, 255, 255))
            
            # Fondo para mejor legibilidad
            (text_width, text_height), _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(
                annotated,
                (10, y_offset - text_height - 5),
                (10 + text_width + 10, y_offset + 5),
                (0, 0, 0),
                -1
            )
            
            # Texto
            cv2.putText(
                annotated,
                text,
                (15, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )
            y_offset += 35
        
        # Agregar valor total si hay billetes colombianos
        total_value = sum(
            int(det['class']) for det in detections 
            if det['is_colombian'] and det['class'].isdigit()
        )
        
        if total_value > 0:
            total_text = f"Total: ${total_value:,} COP"
            cv2.rectangle(
                annotated,
                (10, y_offset - 25),
                (300, y_offset + 10),
                (0, 255, 0),
                -1
            )
            cv2.putText(
                annotated,
                total_text,
                (15, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                2
            )
        
        return annotated
