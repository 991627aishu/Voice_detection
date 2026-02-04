# Deployment Guide

This guide will help you deploy the AI Voice Detection System to production.

## 🚀 Deployment Options

### Option 1: Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set API_KEY=your_secret_api_key_here
   ```

4. **Create Procfile**
   ```
   web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

### Option 2: Deploy to Railway

1. **Connect Repository**
   - Go to https://railway.app
   - Connect your GitHub repository

2. **Configure Environment**
   - Set `API_KEY` in Railway dashboard
   - Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

3. **Deploy**
   - Railway will automatically deploy on push

### Option 3: Deploy to AWS/GCP/Azure

#### AWS (EC2 + S3)

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.micro or larger

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements.txt
   ```

3. **Set Up Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Run with PM2 or systemd**
   ```bash
   pm2 start "uvicorn backend.main:app --host 0.0.0.0 --port 8000" --name voice-detection-api
   ```

#### Google Cloud Platform (Cloud Run)

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY backend/ ./backend/
   CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

2. **Deploy**
   ```bash
   gcloud run deploy voice-detection-api --source .
   ```

### Option 4: Deploy to DigitalOcean App Platform

1. **Create App**
   - Connect repository
   - Select Python buildpack

2. **Configure**
   - Set environment variable: `API_KEY`
   - Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

## 🔧 Frontend Deployment

### Option 1: Netlify

1. **Connect Repository**
   - Go to https://netlify.com
   - Connect your GitHub repository

2. **Configure**
   - Build command: (none needed)
   - Publish directory: `frontend`
   - Add environment variable: `VITE_API_URL` (if using Vite)

3. **Update API URL**
   - Change `API_URL` in `frontend/script.js` to your backend URL

### Option 2: Vercel

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

### Option 3: GitHub Pages

1. **Update script.js**
   ```javascript
   const API_URL = 'https://your-backend-url.com/api/voice-detection';
   ```

2. **Deploy**
   ```bash
   git subtree push --prefix frontend origin gh-pages
   ```

## 🔒 Security Checklist

- [ ] Change default API key
- [ ] Use HTTPS for all connections
- [ ] Set up rate limiting
- [ ] Add request size limits
- [ ] Enable CORS only for your frontend domain
- [ ] Use environment variables for secrets
- [ ] Set up monitoring and logging
- [ ] Regular security updates

## 📊 Monitoring

### Recommended Tools

1. **Sentry** - Error tracking
2. **Datadog** - Performance monitoring
3. **LogRocket** - Frontend monitoring

### Health Check Endpoint

```bash
curl https://your-api.com/health
```

## 🐳 Docker Deployment

### Backend Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
docker build -t voice-detection-api .
docker run -p 8000:8000 -e API_KEY=your_key voice-detection-api
```

## 📝 Environment Variables

Required:
- `API_KEY` - Your secret API key

Optional:
- `PORT` - Server port (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)

## 🚨 Troubleshooting

### Backend won't start
- Check Python version (3.8+)
- Verify all dependencies installed
- Check port availability

### Frontend can't connect
- Verify CORS settings
- Check API URL is correct
- Ensure backend is running

### Audio processing fails
- Verify librosa dependencies
- Check audio file format
- Ensure sufficient memory

## 📞 Support

For issues or questions, check the README.md or open an issue.

