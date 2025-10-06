import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 segundos
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Predecir imagen de billete
 * @param {File} file - Archivo de imagen
 * @returns {Promise} Respuesta con predicciones
 */
export const predictImage = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  } catch (error) {
    console.error('Error en predictImage:', error)
    throw new Error(
      error.response?.data?.error || 
      'Error al comunicarse con el servidor'
    )
  }
}

/**
 * Verificar estado del servidor
 * @returns {Promise} Estado del servidor
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Error en checkHealth:', error)
    throw error
  }
}

export default api
