import { useState } from 'react'
import { predictImage } from '../services/api'
import './ImageUpload.css'

function ImageUpload() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedFile(file)
      setPreview(URL.createObjectURL(file))
      setResult(null)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Por favor selecciona una imagen')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await predictImage(selectedFile)
      setResult(response)
    } catch (err) {
      setError(err.message || 'Error al procesar la imagen')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setPreview(null)
    setResult(null)
    setError(null)
  }

  return (
    <div className="image-upload">
      <div className="upload-section">
        <div className="upload-area">
          <input
            type="file"
            id="file-input"
            accept="image/*"
            onChange={handleFileSelect}
            className="file-input"
          />
          <label htmlFor="file-input" className="file-label">
            <div className="upload-icon">📁</div>
            <p>Click para seleccionar una imagen</p>
            <span className="file-hint">JPG, PNG, JPEG - Max 10MB</span>
          </label>
        </div>

        {preview && (
          <div className="preview-section">
            <h3>Vista Previa:</h3>
            <img src={preview} alt="Preview" className="preview-image" />
          </div>
        )}

        <div className="button-group">
          <button
            onClick={handleUpload}
            disabled={!selectedFile || loading}
            className="btn btn-primary"
          >
            {loading ? '🔄 Clasificando...' : '🚀 Clasificar Billete'}
          </button>
          {selectedFile && (
            <button onClick={handleReset} className="btn btn-secondary">
              🔄 Limpiar
            </button>
          )}
        </div>

        {error && (
          <div className="alert alert-error">
            ❌ {error}
          </div>
        )}
      </div>

      {result && (
        <div className="results-section">
          <h2>📊 Resultados</h2>
          
          <div className="result-image">
            <img src={result.annotated_image} alt="Resultado" />
          </div>

          <div className="stats">
            <div className="stat-card">
              <div className="stat-label">Billetes Detectados</div>
              <div className="stat-value">{result.total_detected}</div>
            </div>
            <div className="stat-card highlight">
              <div className="stat-label">Valor Total</div>
              <div className="stat-value">
                ${result.total_value.toLocaleString('es-CO')} COP
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Tiempo</div>
              <div className="stat-value">{result.inference_time}ms</div>
            </div>
          </div>

          {result.detections.length > 0 && (
            <div className="detections">
              <h3>🔍 Detecciones:</h3>
              {result.detections.map((detection, index) => (
                <div
                  key={index}
                  className={`detection-card ${detection.is_colombian ? 'colombian' : 'foreign'}`}
                >
                  <div className="detection-icon">
                    {detection.is_colombian ? '💵' : '❓'}
                  </div>
                  <div className="detection-info">
                    <div className="detection-message">{detection.message}</div>
                    <div className="detection-confidence">
                      Confianza: {detection.confidence}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ImageUpload
