# Modelo YOLO

## Instrucciones

1. Copia tu archivo `best.pt` a esta carpeta:
   ```
   billetes-classifier-app/backend/ml/best.pt
   ```

2. El modelo será cargado automáticamente al iniciar el servidor.

## Información del Modelo

- **Framework**: YOLOv8/v11 (Ultralytics)
- **Clases**: Billetes colombianos (1000, 2000, 5000, 10000, 20000, 50000, 100000)
- **Input**: Imágenes RGB de cualquier tamaño
- **Output**: Detecciones con bounding boxes y clasificaciones
