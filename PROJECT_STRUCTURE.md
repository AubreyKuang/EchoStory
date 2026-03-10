# EchoStory - Project Structure

```
EchoStory/
│
├── README.md                          # Original project proposal
├── demo.md                            # Demo requirements (Chinese)
├── README_IMPLEMENTATION.md           # Implementation guide (THIS FILE)
├── QUICKSTART.md                      # Quick start guide
├── ARCHITECTURE.md                    # Technical architecture
├── DEPLOYMENT_CHECKLIST.md            # Hackathon checklist
├── PROJECT_STRUCTURE.md               # This file
├── .gitignore                         # Git ignore rules
├── docker-compose.yml                 # Local multi-container setup
│
├── backend/                           # Python/FastAPI backend
│   ├── Dockerfile                     # Backend container config
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment template
│   │
│   └── app/                           # Application code
│       ├── __init__.py
│       ├── main.py                    # FastAPI app entry point
│       ├── config.py                  # Configuration management
│       ├── websocket_handler.py       # WebSocket orchestration
│       │
│       └── services/                  # Service layer
│           ├── __init__.py
│           ├── gemini_service.py      # Gemini Live API integration
│           ├── storage_service.py     # Cloud Storage operations
│           └── firestore_service.py   # Firestore database operations
│
├── frontend/                          # Next.js/React frontend
│   ├── Dockerfile                     # Frontend container config
│   ├── package.json                   # Node dependencies
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── next.config.js                 # Next.js configuration
│   ├── tailwind.config.js             # Tailwind CSS (sensory-friendly theme)
│   ├── postcss.config.js              # PostCSS configuration
│   ├── .env.example                   # Environment template
│   │
│   ├── public/                        # Static assets
│   │
│   └── src/                           # Source code
│       ├── app/                       # Next.js app directory
│       │   ├── page.tsx               # Main application page
│       │   └── layout.tsx             # Root layout
│       │
│       ├── components/                # React components
│       │   ├── LiveCanvas.tsx         # Story display canvas
│       │   ├── ControlPanel.tsx       # Voice/vision controls
│       │   └── CameraOverlay.tsx      # Camera feed overlay
│       │
│       ├── hooks/                     # Custom React hooks
│       │   ├── useWebSocket.ts        # WebSocket connection hook
│       │   ├── useAudioRecorder.ts    # Audio recording hook
│       │   └── useVideoCapture.ts     # Camera capture hook
│       │
│       ├── services/                  # Service layer
│       │   └── websocket.ts           # WebSocket service
│       │
│       ├── types/                     # TypeScript definitions
│       │   └── index.ts               # Shared type definitions
│       │
│       └── styles/                    # Styling
│           └── globals.css            # Global styles
│
├── deployment/                        # Cloud deployment configs
│   └── cloudbuild.yaml                # Google Cloud Build config
│
└── scripts/                           # Utility scripts
    ├── deploy.sh                      # Automated GCP deployment
    └── setup-local.sh                 # Local development setup
```

## File Descriptions

### Root Level

- **README.md**: Original project proposal with background and vision
- **QUICKSTART.md**: Step-by-step guide to get started
- **ARCHITECTURE.md**: Technical architecture documentation
- **DEPLOYMENT_CHECKLIST.md**: Hackathon submission checklist
- **docker-compose.yml**: Local development multi-container setup

### Backend (`backend/`)

#### Main Application
- **app/main.py**: FastAPI application with WebSocket endpoints, health checks, and session management
- **app/config.py**: Centralized configuration using Pydantic settings
- **app/websocket_handler.py**: WebSocket connection manager and message router

#### Services
- **services/gemini_service.py**:
  - Gemini Live API integration
  - Function calling setup
  - Real-time audio/video processing
  - Imagen 3 illustration generation
  - Interruption handling

- **services/storage_service.py**:
  - Cloud Storage operations
  - Image upload and management
  - Asset URL generation

- **services/firestore_service.py**:
  - Session persistence
  - Story segment storage
  - Query and retrieval operations

#### Configuration
- **Dockerfile**: Production container configuration
- **requirements.txt**: Python dependencies (FastAPI, Google AI SDK, etc.)
- **.env.example**: Environment variable template

### Frontend (`frontend/`)

#### Pages & Layouts
- **src/app/page.tsx**: Main application page integrating all components
- **src/app/layout.tsx**: Root layout with metadata and global styling

#### Components
- **components/LiveCanvas.tsx**:
  - Story display with interleaved illustrations
  - Emotion-based background changes
  - Smooth animations and transitions
  - Progress indicators

- **components/ControlPanel.tsx**:
  - Voice recording controls
  - Camera toggle
  - Interruption button
  - Connection status

- **components/CameraOverlay.tsx**:
  - Live video feed display
  - Object detection overlay
  - Recording indicator

#### Hooks
- **hooks/useWebSocket.ts**: WebSocket connection management with React
- **hooks/useAudioRecorder.ts**: Audio recording using MediaRecorder API
- **hooks/useVideoCapture.ts**: Camera capture and frame extraction

#### Services
- **services/websocket.ts**: WebSocket service layer with message handling

#### Types
- **types/index.ts**: TypeScript type definitions for messages, sessions, segments

#### Configuration
- **Dockerfile**: Production container with multi-stage build
- **package.json**: Dependencies (Next.js, React, Framer Motion, etc.)
- **tsconfig.json**: TypeScript compiler options
- **tailwind.config.js**: Custom sensory-friendly color palette
- **postcss.config.js**: PostCSS with Tailwind integration

### Deployment (`deployment/`)

- **cloudbuild.yaml**: Google Cloud Build configuration for CI/CD

### Scripts (`scripts/`)

- **deploy.sh**: Automated deployment to Google Cloud Platform
- **setup-local.sh**: Local development environment setup

## Key Technologies by Component

### Backend Stack
- **Framework**: FastAPI (async web framework)
- **Language**: Python 3.11
- **AI**: Google Generative AI SDK, Vertex AI
- **Database**: Firestore (NoSQL)
- **Storage**: Google Cloud Storage
- **Server**: Uvicorn (ASGI server)

### Frontend Stack
- **Framework**: Next.js 14 (React)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animation**: Framer Motion
- **State**: React Hooks + Custom hooks
- **Communication**: WebSocket (socket.io-client)

### Infrastructure
- **Hosting**: Google Cloud Run
- **Build**: Google Cloud Build
- **Secrets**: Google Secret Manager
- **Containerization**: Docker

## Development Workflow

1. **Local Development**:
   ```bash
   # Terminal 1: Backend
   cd backend && python -m uvicorn app.main:app --reload

   # Terminal 2: Frontend
   cd frontend && npm run dev
   ```

2. **Docker Development**:
   ```bash
   docker-compose up
   ```

3. **Production Deployment**:
   ```bash
   ./scripts/deploy.sh
   ```

## Important Notes

### Environment Variables
- Backend requires: `GOOGLE_CLOUD_PROJECT`, `GEMINI_API_KEY`, `STORAGE_BUCKET_NAME`
- Frontend requires: `NEXT_PUBLIC_WS_URL`, `NEXT_PUBLIC_API_URL`
- Use `.env.example` files as templates

### Dependencies
- Python 3.11+ required for backend
- Node.js 20+ required for frontend
- Docker optional but recommended

### Cloud Services
- Vertex AI API must be enabled
- Firestore database must be initialized
- Storage bucket must be created
- Service account with proper IAM roles required

## File Count Summary

- Backend Python files: 6
- Frontend TypeScript/TSX files: 13
- Configuration files: 10
- Documentation files: 7
- Deployment scripts: 3

**Total Lines of Code**: ~3,500 lines (excluding dependencies)

## Getting Started

1. Review [QUICKSTART.md](./QUICKSTART.md) for setup instructions
2. Check [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details
3. Follow [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) for hackathon submission
4. Read [README_IMPLEMENTATION.md](./README_IMPLEMENTATION.md) for implementation guide
