import { useState, useRef, useEffect } from 'react'
import './CameraStream.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function CameraStream() {
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)
  const [cameraPermission, setCameraPermission] = useState(null)
  
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const wsRef = useRef(null)
  const streamRef = useRef(null)
  const intervalRef = useRef(null)

  useEffect(() => {
    // Cleanup al desmontar
    return () => {
      stopStreaming()
    }
  }, [])

  const startStreaming = async () => {
    try {
      setError(null)
      
      // Solicitar acceso a la cámara con configuración flexible
      let stream = null
      
      try {
        // Primero intentar con preferencia de cámara trasera (móviles)
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: 640 },
            height: { ideal: 480 },
            facingMode: { ideal: 'environment' }
          }
        })
      } catch (err) {
        console.log('⚠️ No se encontró cámara trasera, intentando con cualquier cámara...')
        // Si falla, intentar con cualquier cámara disponible (webcams USB)
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: 640 },
            height: { ideal: 480 }
          }
        })
      }
      
      streamRef.current = stream
      setCameraPermission(true)
      
      console.log('✅ Cámara iniciada correctamente')
      
      // Cambiar estado para renderizar el video
      setIsStreaming(true)
      
      // Esperar a que el video se renderice antes de asignar el stream
      await new Promise(resolve => setTimeout(resolve, 100))
      
      // Asignar el stream al elemento de video
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        console.log('✅ Stream asignado al video')
      } else {
        throw new Error('El elemento de video no está disponible')
      }
      
      // Conectar WebSocket
      const ws = new WebSocket(`${API_URL.replace('http', 'ws')}/ws/predict`)
      wsRef.current = ws
      
      ws.onopen = () => {
        console.log('✅ WebSocket conectado')
        startSendingFrames()
      }
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.success) {
          setResult(data)
        } else if (data.error) {
          console.error('Error del servidor:', data.error)
        }
      }
      
      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
        setError('Error en la conexión WebSocket')
        stopStreaming()
      }
      
      ws.onclose = () => {
        console.log('🔌 WebSocket desconectado')
        setIsStreaming(false)
      }
      
    } catch (err) {
      console.error('❌ Error al acceder a la cámara:', err)
      setError('No se pudo acceder a la cámara. Verifica los permisos.')
      setCameraPermission(false)
      setIsStreaming(false)
      
      // Limpiar el stream si hubo error
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
        streamRef.current = null
      }
    }
  }

  const startSendingFrames = () => {
    // Enviar frames cada 200ms (5 fps)
    intervalRef.current = setInterval(() => {
      if (wsRef.current?.readyState === WebSocket.OPEN && videoRef.current) {
        captureAndSendFrame()
      }
    }, 200)
  }

  const captureAndSendFrame = () => {
    const video = videoRef.current
    const canvas = canvasRef.current
    
    if (!video || !canvas) return
    
    const context = canvas.getContext('2d')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    context.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    // Convertir a base64 y enviar
    canvas.toBlob((blob) => {
      if (blob) {
        const reader = new FileReader()
        reader.onloadend = () => {
          if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(reader.result)
          }
        }
        reader.readAsDataURL(blob)
      }
    }, 'image/jpeg', 0.8)
  }

  const stopStreaming = () => {
    // Detener intervalo
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
    
    // Cerrar WebSocket
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    
    // Detener stream de video
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    
    setIsStreaming(false)
    setResult(null)
  }

  return (
    <div className="camera-stream">
      <div className="camera-section">
        {!isStreaming ? (
          <div className="camera-placeholder">
            <div className="camera-icon">📹</div>
            <h3>Clasificación en Tiempo Real</h3>
            <p>Apunta la cámara a un billete colombiano</p>
            <button onClick={startStreaming} className="btn btn-start">
              🎥 Iniciar Cámara
            </button>
          </div>
        ) : (
          <div className="camera-container">
            <div className="video-wrapper">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="video-stream"
              />
              {result?.annotated_image && (
                <img
                  src={result.annotated_image}
                  alt="Processed"
                  className="processed-overlay"
                />
              )}
            </div>
            
            <button onClick={stopStreaming} className="btn btn-stop">
              ⏹️ Detener Cámara
            </button>
          </div>
        )}
        
        <canvas ref={canvasRef} style={{ display: 'none' }} />
      </div>

      {error && (
        <div className="alert alert-error">
          ❌ {error}
        </div>
      )}

      {isStreaming && result && (
        <div className="live-results">
          <h3>📊 Resultados en Vivo</h3>
          
          <div className="live-stats">
            <div className="stat-badge">
              <span className="badge-label">Detectados:</span>
              <span className="badge-value">{result.total_detected}</span>
            </div>
            <div className="stat-badge highlight">
              <span className="badge-label">Total:</span>
              <span className="badge-value">
                ${result.total_value.toLocaleString('es-CO')}
              </span>
            </div>
            <div className="stat-badge">
              <span className="badge-label">FPS:</span>
              <span className="badge-value">{result.fps}</span>
            </div>
          </div>

          {result.detections.length > 0 && (
            <div className="live-detections">
              {result.detections.map((detection, index) => (
                <div
                  key={index}
                  className={`live-detection ${detection.is_colombian ? 'colombian' : 'foreign'}`}
                >
                  <span className="detection-emoji">
                    {detection.is_colombian ? '💵' : '❓'}
                  </span>
                  <span className="detection-text">
                    {detection.class} ({detection.confidence}%)
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {cameraPermission === false && (
        <div className="alert alert-warning">
          ⚠️ Necesitas permitir el acceso a la cámara para usar esta función.
          <br />
          <small>Ve a la configuración de tu navegador para activar los permisos.</small>
        </div>
      )}
    </div>
  )
}

export default CameraStream
