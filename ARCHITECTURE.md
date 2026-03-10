# EchoStory - Technical Architecture

## Overview

EchoStory is a multimodal AI Live Agent that helps children with ASD tell stories through real-time voice and visual interactions.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Live Canvas  │  │ Voice Input  │  │ Video Input  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────────┬─────────────────────────────────┘
                            │ WebSocket (Full-Duplex)
┌───────────────────────────▼─────────────────────────────────┐
│                   Backend (FastAPI + WebSocket)              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         WebSocket Handler (Orchestrator)             │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                 │
│  ┌─────────────┬───────────┴───────────┬─────────────┐    │
│  │             │                        │              │    │
│  ▼             ▼                        ▼              ▼    │
│ ┌─────┐   ┌─────────┐   ┌──────────┐  ┌──────────┐       │
│ │Gemini│   │ Imagen  │   │ Storage  │  │Firestore │       │
│ │ Live │   │   3     │   │ Service  │  │ Service  │       │
│ └─────┘   └─────────┘   └──────────┘  └──────────┘       │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                  Google Cloud Platform                       │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Cloud   │  │ Vertex   │  │  Cloud   │  │Firestore │   │
│  │  Run    │  │   AI     │  │ Storage  │  │          │   │
│  └─────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend (React/Next.js)

#### Live Canvas Component
- **Purpose**: Real-time visual storybook display
- **Features**:
  - Interleaved illustration + text rendering
  - Emotion-based background color changes
  - Smooth animations (fade-in/slide-up)
  - Progress indicators

#### Voice/Vision Controls
- **Audio Recording**: WebRTC MediaRecorder API
- **Video Capture**: Live camera feed with frame extraction
- **Interruption**: Real-time interrupt button

#### WebSocket Service
- Persistent connection management
- Message routing (audio, video, text)
- Automatic reconnection logic

### 2. Backend (FastAPI)

#### WebSocket Handler
- **Connection Management**: Session-based connections
- **Message Router**: Routes messages by type
- **State Management**: Tracks generation state per session

#### Gemini Service
- **Live API Integration**: Real-time voice processing
- **System Instructions**: "Gentle Playmate" persona
- **Function Calling**: Triggers for illustration generation
- **Vision Analysis**: Object detection from camera frames
- **Interruption Handling**: Stops active streams

#### Storage Service
- **Image Upload**: Base64 → Cloud Storage
- **Asset Management**: Session-based organization
- **Public URLs**: Generated for frontend access

#### Firestore Service
- **Session Persistence**: Story journal storage
- **Segment Management**: Real-time story segment saves
- **Query Support**: List/filter sessions

### 3. Cloud Infrastructure (GCP)

#### Cloud Run
- **Containerized Deployment**: Docker-based
- **Auto-scaling**: Based on demand
- **Region**: us-central1

#### Vertex AI
- **Gemini 2.0 Flash**: Live voice + vision model
- **Imagen 3**: Child-friendly illustration generation

#### Cloud Storage
- **Asset Storage**: Images, audio files
- **Public Access**: Direct URL serving

#### Firestore
- **NoSQL Database**: Session and segment storage
- **Real-time Updates**: Live synchronization

## Key Innovations

### 1. Interleaved Output
- **Problem**: Traditional AI outputs are turn-based
- **Solution**: Stream text, audio, and images simultaneously
- **Implementation**: Function calling triggers concurrent image generation while voice continues

### 2. Live Vision Integration
- **Problem**: Static text-only interaction
- **Solution**: Real-time object detection from camera
- **Implementation**: Frame extraction → Gemini Vision → Proactive story integration

### 3. Interruption Support
- **Problem**: Children need to change direction mid-story
- **Solution**: Real-time interrupt handling
- **Implementation**: WebSocket interrupt message → Stop generation → Re-contextualize

### 4. Low-Demand Design
- **Problem**: Traditional tools pressure children to perform
- **Solution**: Accept any input (words, sounds, gestures)
- **Implementation**: Flexible input handling + validation-focused prompts

## Data Flow

### Story Creation Flow

```
1. User speaks → Audio chunk → WebSocket
2. Backend → Gemini Live API (streaming)
3. Gemini decides → Call generate_illustration()
4. Parallel execution:
   - Continue voice narration stream
   - Generate image with Imagen 3
   - Upload to Cloud Storage
5. Send image URL → Frontend (WebSocket)
6. Frontend renders image + text simultaneously
7. Save segment to Firestore
```

### Vision Detection Flow

```
1. Camera active → Capture frame every 3s
2. Frame → WebSocket → Backend
3. Gemini Vision analyzes frame
4. Object detected → Generate proactive prompt
5. Send detection → Frontend
6. AI mentions object in story
```

## Security & Privacy

### Safety Filters
- Gemini safety settings: BLOCK_MEDIUM_AND_ABOVE
- Child-safe content validation
- No PII collection without consent

### Data Storage
- Session data: Firestore (encrypted at rest)
- Images: Cloud Storage (private unless shared)
- No audio recording storage (streaming only)

### Access Control
- Cloud Run: Authenticated endpoints
- Storage: Signed URLs for sensitive data
- Firestore: Security rules for user data

## Performance Optimization

### Latency Targets
- Voice response: <500ms
- Image generation: 2-5s
- Frame analysis: <1s

### Caching
- WebSocket connection pooling
- Gemini session context caching
- Frontend asset caching

### Scalability
- Stateless backend (Cloud Run auto-scaling)
- Session state in Firestore
- Asset delivery via CDN (Cloud Storage)

## Development Workflow

### Local Development
1. Run backend: `uvicorn app.main:app --reload`
2. Run frontend: `npm run dev`
3. Or use Docker Compose: `docker-compose up`

### Deployment
1. Configure GCP project
2. Set environment variables
3. Run: `./scripts/deploy.sh`
4. Cloud Build handles build + deploy

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14, React, TypeScript | UI framework |
| Styling | Tailwind CSS, Framer Motion | Sensory-friendly design + animations |
| Backend | FastAPI, Python 3.11 | Async WebSocket server |
| AI Models | Gemini 2.0 Flash, Imagen 3 | Voice, vision, image generation |
| Database | Firestore | Session storage |
| Storage | Cloud Storage | Asset storage |
| Hosting | Cloud Run | Containerized deployment |
| Build | Docker, Cloud Build | CI/CD pipeline |

## Future Enhancements

1. **Video Generation**: Integrate Veo for 3-5s animated clips
2. **Parent Dashboard**: View child's daily stories
3. **Emotion Analytics**: Track emotional patterns over time
4. **Multi-language**: Support for multiple languages
5. **Offline Mode**: Local storage for areas with poor connectivity
