# 🚀 Guía Rápida de Inicio

## Pasos Iniciales (5 minutos)

### 1. Copiar tu modelo entrenado

```bash
# Desde la carpeta raíz
copy ..\best.pt backend\ml\best.pt
```

### 2. Iniciar Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

✅ Backend corriendo en: http://localhost:8000

### 3. Iniciar Frontend (nueva terminal)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend corriendo en: http://localhost:5173

### 4. ¡A probar!

Abre http://localhost:5173 en tu navegador y empieza a clasificar billetes 💵

---

## Comandos Útiles

```bash
# Ver documentación API
http://localhost:8000/docs

# Verificar salud del backend
http://localhost:8000/health

# Build para producción (frontend)
cd frontend
npm run build

# Docker (todo en uno)
docker-compose up --build
```

---

## Troubleshooting Rápido

❌ **Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

❌ **Error: npm command not found**
- Instala Node.js desde https://nodejs.org

❌ **Puerto 8000 en uso**
```bash
# Cambiar puerto en backend/app.py línea final
uvicorn.run("app:app", host="0.0.0.0", port=8001)
```

❌ **Modelo no carga**
- Verifica que `best.pt` esté en `backend/ml/`

---

## Próximo Paso: Deploy

Lee el README.md principal para instrucciones de despliegue en:
- Vercel (Frontend)
- Railway (Backend)
- Render (Ambos)
