from ultralytics import YOLO
import cv2
import time
import torch

# Verificar si GPU está disponible
print("✅ GPU disponible:", torch.cuda.is_available())

# Cargar el modelo YOLO personalizado
model = YOLO("best.pt")


# Elegir índice de cámara
cam_index = int(input("Ingresa el número de cámara (0=PC, 1=móvil, etc): "))
cap = cv2.VideoCapture(cam_index)

# Configurar resolución y FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ No se pudo leer el frame de la cámara.")
        break

    # Redimensionar frame para mejorar velocidad
    frame = cv2.resize(frame, (640, 480))

    # Medir tiempo de inferencia
    start = time.time()

    # Inferencia YOLO
    results = model(frame)


    # Etiquetas válidas de billetes colombianos
    etiquetas_col = {"1000", "2000", "5000", "10000", "20000", "50000", "100000"}
    mensajes = []

    # Procesar resultados
    for box in results[0].boxes:
        clase_idx = int(box.cls[0])
        clase_nombre = results[0].names[clase_idx]
        if clase_nombre in etiquetas_col:
            mensaje = f"Billete colombiano: {clase_nombre}"
        else:
            mensaje = f"Billete de otra moneda o desconocido: {clase_nombre}"
        mensajes.append(mensaje)

    # Dibujar resultados
    annotated_frame = results[0].plot()

    # Mostrar mensajes en la ventana del video
    y0 = 60
    for i, mensaje in enumerate(mensajes):
        y = y0 + i * 30
        cv2.putText(annotated_frame, mensaje, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Calcular y mostrar FPS
    end = time.time()
    fps = 1 / (end - start)
    cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar resultado
    cv2.imshow("YOLO Inference", annotated_frame)

    # Salir con ESC (tecla 27)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
