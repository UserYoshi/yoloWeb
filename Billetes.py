from ultralytics import YOLO
import cv2
import time
import torch

# --- Constantes de Configuración ---
MODEL_PATH = "best.pt"
CONF_THRESHOLD = 0.6  # Umbral de confianza, ajústalo según tus pruebas (0.5, 0.6, 0.7)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FONT = cv2.FONT_HERSHEY_SIMPLEX
ETIQUETAS_VALIDAS = {"1000", "2000", "5000", "10000", "20000", "50000", "100000"}

def main():
    """Función principal para ejecutar la detección de billetes."""
    # Verificar si GPU está disponible
    print("✅ GPU disponible:", torch.cuda.is_available())

    # Cargar el modelo YOLO personalizado
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"❌ Error al cargar el modelo '{MODEL_PATH}': {e}")
        return

    # Elegir índice de cámara
    try:
        cam_index = int(input("Ingresa el número de cámara (0=PC, 1=móvil, etc): "))
    except ValueError:
        print("❌ Entrada no válida. Usando cámara 0 por defecto.")
        cam_index = 0

    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"❌ No se pudo abrir la cámara con índice {cam_index}.")
        return

    # Configurar resolución y FPS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("❌ No se pudo leer el frame de la cámara. Saliendo...")
            break

        # Redimensionar frame asegura un tamaño consistente
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        start_time = time.time()

        # Inferencia YOLO con umbral de confianza
        results = model(frame, conf=CONF_THRESHOLD, verbose=False)

        # Dibujar resultados directamente con el método plot() de Ultralytics
        annotated_frame = results[0].plot()

        # Procesar y mostrar mensajes personalizados
        mensajes = []
        for box in results[0].boxes:
            clase_nombre = model.names[int(box.cls[0])]
            if clase_nombre in ETIQUETAS_VALIDAS:
                mensaje = f"Billete colombiano: {clase_nombre}"
            else:
                mensaje = f"Detectado: {clase_nombre}"
            mensajes.append(mensaje)

        for i, mensaje in enumerate(mensajes):
            cv2.putText(annotated_frame, mensaje, (10, 60 + i * 30), FONT, 0.9, (0, 0, 255), 2)

        # Calcular y mostrar FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time) if (end_time - start_time) > 0 else 0
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), FONT, 1, (0, 255, 0), 2)

        cv2.imshow("Detector de Billetes", annotated_frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Salir con ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
