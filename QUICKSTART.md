# EchoStory - Quick Start Guide

## Prerequisites

### Required
- Python 3.11+
- Node.js 20+
- Google Cloud Platform account
- Gemini API key

### Optional
- Docker & Docker Compose
- Google Cloud SDK (`gcloud`)

## Local Development Setup

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./scripts/setup-local.sh

# Update backend/.env with your credentials
# Update frontend/.env.local if needed
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your credentials:
# - GOOGLE_CLOUD_PROJECT
# - GEMINI_API_KEY
# - GOOGLE_APPLICATION_CREDENTIALS (path to service account JSON)
# - STORAGE_BUCKET_NAME
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.example .env.local

# Default values should work for local development
```

## Running the Application

### Option 1: Using Docker Compose (Easiest)

```bash
# Set environment variables
export GOOGLE_CLOUD_PROJECT=your-project-id
export GEMINI_API_KEY=your-api-key
export STORAGE_BUCKET_NAME=your-bucket
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Start all services
docker-compose up
```

Access the app:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Run Separately

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Google Cloud Setup

### 1. Create GCP Project

```bash
# Set project ID
export PROJECT_ID=echostory-demo

# Create project
gcloud projects create $PROJECT_ID

# Set current project
gcloud config set project $PROJECT_ID

# Enable billing (required)
# Go to: https://console.cloud.google.com/billing
```

### 2. Enable Required APIs

```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    aiplatform.googleapis.com \
    firestore.googleapis.com \
    storage.googleapis.com
```

### 3. Create Service Account

```bash
# Create service account
gcloud iam service-accounts create echostory-sa \
    --display-name="EchoStory Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:echostory-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:echostory-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:echostory-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create and download key
gcloud iam service-accounts keys create credentials.json \
    --iam-account=echostory-sa@$PROJECT_ID.iam.gserviceaccount.com
```

### 4. Create Cloud Storage Bucket

```bash
# Create bucket
gsutil mb -p $PROJECT_ID -l us-central1 gs://echostory-assets-$PROJECT_ID

# Make publicly readable
gsutil iam ch allUsers:objectViewer gs://echostory-assets-$PROJECT_ID
```

### 5. Initialize Firestore

```bash
# Create Firestore database
gcloud firestore databases create --region=us-central1
```

### 6. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key

## Deployment to Cloud Run

### Automated Deployment

```bash
# Set environment variables
export GOOGLE_CLOUD_PROJECT=your-project-id
export GEMINI_API_KEY=your-api-key
export STORAGE_BUCKET_NAME=echostory-assets-your-project-id

# Run deployment script
./scripts/deploy.sh
```

### Manual Deployment

```bash
# Build and push backend
gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/echostory-backend \
    ./backend

# Deploy backend to Cloud Run
gcloud run deploy echostory-backend \
    --image gcr.io/$PROJECT_ID/echostory-backend \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated

# Get backend URL
BACKEND_URL=$(gcloud run services describe echostory-backend \
    --region us-central1 \
    --format='value(status.url)')

# Build and push frontend (update env vars first)
gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/echostory-frontend \
    ./frontend

# Deploy frontend
gcloud run deploy echostory-frontend \
    --image gcr.io/$PROJECT_ID/echostory-frontend \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe echostory-frontend \
    --region us-central1 \
    --format='value(status.url)')

echo "Backend: $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
```

## Testing the Application

### 1. Test WebSocket Connection

```bash
# Install wscat
npm install -g wscat

# Connect to WebSocket
wscat -c ws://localhost:8000/ws/story
```

### 2. Test REST Endpoints

```bash
# Health check
curl http://localhost:8000/health

# List sessions
curl http://localhost:8000/api/sessions
```

### 3. Test Frontend

1. Open http://localhost:3000
2. Click the orange microphone button
3. Say "I went to the park today"
4. Watch the AI respond and generate illustrations

## Troubleshooting

### Backend Issues

**Issue: Import errors**
```bash
# Make sure you're in the virtual environment
source backend/venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

**Issue: Google Cloud authentication**
```bash
# Set credentials environment variable
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Or use gcloud auth
gcloud auth application-default login
```

**Issue: WebSocket connection refused**
- Check if backend is running on port 8000
- Check firewall settings
- Verify CORS settings in backend/app/main.py

### Frontend Issues

**Issue: WebSocket connection failed**
- Verify backend is running
- Check NEXT_PUBLIC_WS_URL in .env.local
- Check browser console for errors

**Issue: Camera not working**
- Allow camera permissions in browser
- Use HTTPS (required for getUserMedia)
- Check browser compatibility

**Issue: Build errors**
```bash
# Clear Next.js cache
rm -rf frontend/.next

# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
```

### Cloud Deployment Issues

**Issue: Permission denied**
```bash
# Re-authenticate
gcloud auth login

# Check current project
gcloud config get-value project

# Verify IAM permissions
gcloud projects get-iam-policy $PROJECT_ID
```

**Issue: Cloud Run deployment fails**
- Check Cloud Build logs in GCP Console
- Verify all APIs are enabled
- Check container logs: `gcloud run logs read echostory-backend`

## Performance Tips

1. **Use HTTP/2**: Cloud Run supports HTTP/2 for better WebSocket performance
2. **Regional Deployment**: Deploy close to your users (default: us-central1)
3. **Image Optimization**: Consider caching generated images
4. **Connection Pooling**: WebSocket reconnection is automatic

## Security Checklist

- [ ] Store API keys in Secret Manager (production)
- [ ] Enable Cloud Armor for DDoS protection
- [ ] Use Cloud IAM for access control
- [ ] Enable audit logging
- [ ] Implement rate limiting
- [ ] Add authentication for user sessions

## Next Steps

1. **Customize the Persona**: Edit `system_instruction` in `backend/app/services/gemini_service.py`
2. **Adjust UI Colors**: Modify Tailwind config in `frontend/tailwind.config.js`
3. **Add More Tools**: Extend function calling in Gemini service
4. **Implement Analytics**: Add tracking for story interactions
5. **Create Demo Video**: Record a 4-minute demo for hackathon submission

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review architecture: See ARCHITECTURE.md
- API documentation: http://localhost:8000/docs

## Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
