# 🚀 Guía de Deployment en Producción

Esta guía te ayudará a desplegar tu aplicación en diferentes plataformas cloud.

## 📋 Índice

1. [Railway (Backend)](#railway-backend)
2. [Vercel (Frontend)](#vercel-frontend)
3. [Render (Full-Stack)](#render-full-stack)
4. [Docker Manual](#docker-manual)

---

## 🚂 Railway (Backend)

Railway es ideal para el backend porque ofrece:
- Plan gratuito con $5 de crédito mensual
- Deploy automático con Dockerfile
- Variables de entorno fáciles

### Pasos:

1. **Crear cuenta**: https://railway.app

2. **Crear nuevo proyecto**:
   ```
   New Project → Deploy from GitHub repo
   ```

3. **Seleccionar carpeta `backend`**

4. **Configurar variables de entorno**:
   ```env
   PORT=8000
   HOST=0.0.0.0
   DEBUG=False
   ALLOWED_ORIGINS=https://tu-frontend.vercel.app
   ```

5. **Railway detectará automáticamente el Dockerfile**

6. **Obtener URL**:
   ```
   Settings → Generate Domain
   Ejemplo: https://billetes-backend.railway.app
   ```

7. **Verificar deployment**:
   ```
   https://tu-backend.railway.app/health
   https://tu-backend.railway.app/docs
   ```

### Subir el modelo `best.pt`:

**Opción 1: Incluir en Git** (si < 100MB)
```bash
cd backend
git add ml/best.pt
git commit -m "Add YOLO model"
git push
```

**Opción 2: Montar volumen en Railway**
- Sube `best.pt` a Google Drive/Dropbox
- En Railway: Settings → Volumes
- Descarga el modelo en el startup script

---

## ▲ Vercel (Frontend)

Vercel es perfecto para el frontend React:
- Plan gratuito generoso
- Deploy automático desde Git
- CDN global

### Pasos:

1. **Crear cuenta**: https://vercel.com

2. **Importar proyecto**:
   ```
   New Project → Import Git Repository
   ```

3. **Configurar build**:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

4. **Variables de entorno**:
   ```env
   VITE_API_URL=https://tu-backend.railway.app
   ```

5. **Deploy automático**:
   - Cada push a main despliega automáticamente

6. **Obtener URL**:
   ```
   https://billetes-classifier.vercel.app
   ```

7. **Configurar dominio personalizado** (opcional):
   - Settings → Domains
   - Agregar tu dominio

### Actualizar CORS en Backend:

Recuerda actualizar las variables de entorno en Railway:
```env
ALLOWED_ORIGINS=https://billetes-classifier.vercel.app
```

---

## 🎨 Render (Full-Stack)

Render permite deployar backend y frontend juntos:

### Backend (Web Service):

1. **Crear cuenta**: https://render.com

2. **New Web Service**:
   ```
   Connect repository → Select backend/
   ```

3. **Configuración**:
   ```
   Name: billetes-backend
   Environment: Docker
   Plan: Free (con limitaciones)
   ```

4. **Variables de entorno**:
   ```env
   PORT=8000
   PYTHON_VERSION=3.10
   ```

5. **Deploy**

6. **URL generada**:
   ```
   https://billetes-backend.onrender.com
   ```

### Frontend (Static Site):

1. **New Static Site**:
   ```
   Connect repository → Select frontend/
   ```

2. **Configuración**:
   ```
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

3. **Variables de entorno**:
   ```env
   VITE_API_URL=https://billetes-backend.onrender.com
   ```

4. **Deploy**

### ⚠️ Nota sobre Render Free:
- El servicio se "duerme" después de 15 minutos de inactividad
- Primera carga puede tardar 30-60 segundos
- Considera plan Starter ($7/mes) para producción

---

## 🐳 Docker Manual (VPS/AWS/GCP/Azure)

Para deployar en tu propio servidor:

### 1. Preparar servidor:

```bash
# Instalar Docker y Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
sudo apt-get install docker-compose-plugin
```

### 2. Clonar repositorio:

```bash
git clone https://github.com/tu-usuario/billetes-classifier-app.git
cd billetes-classifier-app
```

### 3. Configurar variables:

**Backend `.env`:**
```env
PORT=8000
HOST=0.0.0.0
DEBUG=False
ALLOWED_ORIGINS=https://tu-dominio.com
```

**Frontend `.env`:**
```env
VITE_API_URL=https://api.tu-dominio.com
```

### 4. Build y Run:

```bash
docker-compose up -d --build
```

### 5. Configurar Nginx (Reverse Proxy):

```nginx
# /etc/nginx/sites-available/billetes
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://localhost:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 6. Habilitar HTTPS con Certbot:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

### 7. Auto-restart:

```bash
# Crear systemd service
sudo nano /etc/systemd/system/billetes.service
```

```ini
[Unit]
Description=Billetes Classifier
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/billetes-classifier-app
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable billetes
sudo systemctl start billetes
```

---

## 📊 Comparación de Plataformas

| Plataforma | Backend | Frontend | Costo | Pros | Contras |
|-----------|---------|----------|-------|------|---------|
| **Railway + Vercel** | ✅ | ✅ | $0-5/mes | Fácil, rápido | Límites de uso |
| **Render** | ✅ | ✅ | $0-7/mes | Todo en uno | Sleep en free |
| **AWS/GCP/Azure** | ✅ | ✅ | $10-50/mes | Escalable | Complejo |
| **VPS (DigitalOcean)** | ✅ | ✅ | $5-10/mes | Control total | Manual |

---

## ✅ Checklist Pre-Deploy

- [ ] Modelo `best.pt` incluido o accesible
- [ ] Variables de entorno configuradas
- [ ] CORS configurado correctamente
- [ ] .gitignore actualizado
- [ ] Dependencias actualizadas
- [ ] Probado localmente con Docker
- [ ] HTTPS habilitado (producción)
- [ ] Monitoring configurado
- [ ] Backups automáticos (si aplica)

---

## 🐛 Troubleshooting Común

### "Cannot connect to backend"
- Verifica la URL en `VITE_API_URL`
- Revisa CORS en backend
- Verifica que el backend esté corriendo

### "Model file not found"
- Verifica que `best.pt` esté en `backend/ml/`
- Revisa los logs del deployment

### "WebSocket connection failed"
- Usa `wss://` en producción (no `ws://`)
- Verifica configuración de proxy/nginx

### "502 Bad Gateway"
- Backend probablemente está caído
- Revisa logs: `docker logs <container>`

---

## 📞 Soporte

Si tienes problemas con el deployment:
1. Revisa los logs del servicio
2. Verifica las variables de entorno
3. Prueba localmente con Docker primero
4. Consulta la documentación de la plataforma específica

---

**¡Feliz Deployment! 🚀**
