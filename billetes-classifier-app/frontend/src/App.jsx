import { useState } from 'react'
import ImageUpload from './components/ImageUpload'
import CameraStream from './components/CameraStream'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('upload')

  return (
    <div className="app">
      <header className="header">
        <h1>💵 Clasificador de Billetes Colombianos</h1>
        <p>Detecta y clasifica billetes colombianos usando Inteligencia Artificial</p>
      </header>

      <div className="tab-container">
        <button
          className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📤 Subir Imagen
        </button>
        <button
          className={`tab ${activeTab === 'camera' ? 'active' : ''}`}
          onClick={() => setActiveTab('camera')}
        >
          📹 Cámara en Tiempo Real
        </button>
      </div>

      <main className="main-content">
        {activeTab === 'upload' ? <ImageUpload /> : <CameraStream />}
      </main>

      <footer className="footer">
        <p>Powered by YOLOv8 + FastAPI + React</p>
        <p className="tech-stack">
          <span>🐍 Python</span>
          <span>⚡ FastAPI</span>
          <span>⚛️ React</span>
          <span>🧠 YOLO</span>
        </p>
      </footer>
    </div>
  )
}

export default App
