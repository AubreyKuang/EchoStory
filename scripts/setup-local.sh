#!/bin/bash

# Local development setup script for EchoStory

set -e

echo "🛠️  EchoStory Local Development Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version"

# Check Node version
echo "Checking Node version..."
node_version=$(node --version)
echo "✅ Node $node_version"

# Setup backend
echo ""
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please update backend/.env with your API keys"
fi

cd ..

# Setup frontend
echo ""
echo "📦 Setting up frontend..."
cd frontend

echo "Installing Node dependencies..."
npm install

echo "Creating .env.local file..."
if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
    echo "✅ Created frontend/.env.local"
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Update backend/.env with your API keys:"
echo "   - GOOGLE_CLOUD_PROJECT"
echo "   - GEMINI_API_KEY"
echo "   - GOOGLE_APPLICATION_CREDENTIALS"
echo "   - STORAGE_BUCKET_NAME"
echo ""
echo "2. Start the development servers:"
echo "   - Backend: cd backend && source venv/bin/activate && python -m app.main"
echo "   - Frontend: cd frontend && npm run dev"
echo ""
echo "   Or use Docker Compose:"
echo "   - docker-compose up"
echo ""
