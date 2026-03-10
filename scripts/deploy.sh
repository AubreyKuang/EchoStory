#!/bin/bash

# EchoStory Deployment Script for Google Cloud Run

set -e

echo "🚀 EchoStory Deployment Script"
echo "================================"

# Check if required environment variables are set
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "❌ Error: GOOGLE_CLOUD_PROJECT is not set"
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY is not set"
    exit 1
fi

if [ -z "$STORAGE_BUCKET_NAME" ]; then
    echo "❌ Error: STORAGE_BUCKET_NAME is not set"
    exit 1
fi

PROJECT_ID=$GOOGLE_CLOUD_PROJECT
REGION="us-central1"

echo "📋 Project: $PROJECT_ID"
echo "📍 Region: $REGION"
echo ""

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com \
    firestore.googleapis.com \
    storage.googleapis.com \
    aiplatform.googleapis.com \
    --project=$PROJECT_ID

# Create storage bucket if it doesn't exist
echo "📦 Setting up Cloud Storage..."
if ! gsutil ls -b gs://$STORAGE_BUCKET_NAME &> /dev/null; then
    gsutil mb -p $PROJECT_ID -l $REGION gs://$STORAGE_BUCKET_NAME
    echo "✅ Bucket created: $STORAGE_BUCKET_NAME"
else
    echo "✅ Bucket already exists: $STORAGE_BUCKET_NAME"
fi

# Make bucket publicly readable
gsutil iam ch allUsers:objectViewer gs://$STORAGE_BUCKET_NAME

# Create Firestore database if it doesn't exist
echo "🗄️  Setting up Firestore..."
gcloud firestore databases create --region=$REGION --project=$PROJECT_ID 2>/dev/null || echo "✅ Firestore database already exists"

# Store Gemini API key in Secret Manager
echo "🔐 Storing secrets..."
echo -n "$GEMINI_API_KEY" | gcloud secrets create gemini-api-key \
    --data-file=- \
    --replication-policy="automatic" \
    --project=$PROJECT_ID 2>/dev/null || \
echo -n "$GEMINI_API_KEY" | gcloud secrets versions add gemini-api-key \
    --data-file=- \
    --project=$PROJECT_ID

echo "✅ Secrets configured"

# Build and deploy using Cloud Build
echo "🏗️  Building and deploying with Cloud Build..."
gcloud builds submit \
    --config=deployment/cloudbuild.yaml \
    --substitutions=_STORAGE_BUCKET=$STORAGE_BUCKET_NAME \
    --project=$PROJECT_ID \
    .

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your services are now running on Google Cloud Run"
echo ""
echo "📝 Next steps:"
echo "1. Get your backend URL: gcloud run services describe echostory-backend --region=$REGION --format='value(status.url)'"
echo "2. Get your frontend URL: gcloud run services describe echostory-frontend --region=$REGION --format='value(status.url)'"
echo "3. Update frontend environment variables with the backend URL"
echo ""
