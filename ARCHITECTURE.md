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
  - Interleaved illustration + text rendering (images 80% width, max-h-[50vh])
  - Emotion-based background color changes
  - Smooth animations (fade-in/slide-up)
  - Progress indicators at bottom
  - Content positioned from top (pt-20 pb-24, justify-start)
  - "Creating magic..." loading indicator in top-right

#### Logo & Session Components
- **Logo**: Top-left corner with ✨ icon and "EchoStory" branding
- **Session Info**: Top-right corner showing current session ID
- **Layout**: Fixed positioning, z-index 50, minimal interference with content

#### Voice/Vision Controls
- **Audio Recording**:
  - WebRTC MediaRecorder API
  - Records continuously, sends complete audio only when stopped
  - No intermediate chunk streaming (prevents UI flashing)
- **Video Capture**:
  - Live camera feed with frame extraction every 3 seconds
  - Uses `streamRef` to store stream before video element renders
  - Connects stream in `useEffect` after element is available
- **Interruption**: Real-time interrupt button
- **Speech Synthesis**: Web Speech API with 200ms delay for text sync

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

## Demo Mode

### Purpose
Demo Mode allows testing and development without requiring:
- Real Gemini API access (important for region-restricted areas)
- Google Cloud credentials
- Cloud Storage/Firestore setup

### Activation
Set `DEMO_MODE=true` in `.env` or environment variables.

### Demo Services

#### DemoGeminiService (`demo_service.py`)
- **Simulates Gemini responses**: Returns predefined story text
- **Mock function calls**: Always triggers illustration generation
- **Timing**: 500ms delay to simulate API latency
- **Behavior**: Only responds when `is_final=true` to prevent UI flashing

#### DemoStorageService
- **Returns input URL directly**: No actual upload to Cloud Storage
- **Local image support**: Works with `http://localhost:3000/test.png`

#### DemoFirestoreService
- **Mock session management**: Returns success without database writes
- **No persistence**: Sessions are not saved

### Configuration Check
```python
# backend/app/main.py
if settings.DEMO_MODE:
    from app.services.demo_service import DemoGeminiService as GeminiService
else:
    from app.services.gemini_service import GeminiService
```

### Required Environment Variables

#### Production Mode
```bash
DEMO_MODE=false
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
GEMINI_API_KEY=your-gemini-api-key
STORAGE_BUCKET_NAME=your-bucket-name
```

#### Demo Mode
```bash
DEMO_MODE=true
# No other credentials required!
```

## Key Innovations

### 1. Interleaved Output
- **Problem**: Traditional AI outputs are turn-based (wait for everything before displaying)
- **Solution**: Display text and play voice immediately, then add image when ready
- **Implementation**:
  1. Gemini responds with text + function call for illustration
  2. Frontend creates segment with text immediately (no image yet)
  3. Text animates in (300ms) and voice starts (200ms delay)
  4. Backend generates image with Imagen 3 in parallel
  5. Image URL sent via WebSocket when ready
  6. Frontend updates existing segment with image (fade-in animation 600ms)
- **Result**: User sees text/hears voice within ~200ms, image appears 2-5s later

### 2. Live Vision Integration
- **Problem**: Static text-only interaction
- **Solution**: Real-time object detection from camera
- **Implementation**:
  - Store MediaStream in `streamRef` before video element renders
  - Set `isCapturing=true` to trigger video element rendering
  - Connect stream to video element in `useEffect`
  - Extract frames every 3 seconds → Gemini Vision → Proactive story integration

### 3. Interruption Support
- **Problem**: Children need to change direction mid-story
- **Solution**: Real-time interrupt handling
- **Implementation**: WebSocket interrupt message → Stop generation → Cancel speech synthesis → Re-contextualize

### 4. Low-Demand Design
- **Problem**: Traditional tools pressure children to perform
- **Solution**: Accept any input (words, sounds, gestures)
- **Implementation**: Flexible input handling + validation-focused prompts

## Data Flow

### Story Creation Flow

```
1. User speaks → Record audio → Stop recording
2. Send complete audio (is_final=true) → WebSocket → Backend
3. Backend → Gemini Live API processes complete audio
4. Gemini responds with text + decides to call generate_illustration()
5. Frontend immediately:
   - Creates story segment with text
   - Displays text with animation
   - Starts TTS playback (200ms delay for sync)
6. Backend parallel execution:
   - Generate image with Imagen 3
   - Upload to Cloud Storage (or return URL in Demo Mode)
7. Send image URL → Frontend (WebSocket)
8. Frontend updates existing segment with image (fade-in animation)
9. Save segment to Firestore (or mock in Demo Mode)
```

**Note**: Audio is sent only when recording stops (not streaming chunks) to prevent UI flashing.

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
- Voice response: <500ms (in Demo Mode)
- Image generation: 2-5s
- Frame analysis: <1s

### UI Optimization
- **Audio Processing**: Send only final audio to prevent frequent UI updates
- **Animation Timing**:
  - Text animation: 300ms
  - Voice playback delay: 200ms (synced with text)
  - Image fade-in: 600ms
- **React Strict Mode**: Disabled to prevent WebSocket double connections

### Caching
- WebSocket connection pooling with `connectingRef` to prevent duplicates
- Gemini session context caching
- Frontend asset caching

### Scalability
- Stateless backend (Cloud Run auto-scaling)
- Session state in Firestore
- Asset delivery via CDN (Cloud Storage)

## Development Workflow

### Local Development

#### With Demo Mode (No API keys required)
1. Set `DEMO_MODE=true` in `backend/.env`
2. Run backend: `cd backend && uvicorn app.main:app --reload`
3. Run frontend: `cd frontend && npm run dev`
4. Test with simulated AI responses

#### With Real APIs
1. Configure GCP credentials and API keys in `backend/.env`
2. Set `DEMO_MODE=false`
3. Run backend: `cd backend && uvicorn app.main:app --reload`
4. Run frontend: `cd frontend && npm run dev`

#### Docker Compose
- `docker-compose up` (uses environment variables from `.env`)

### Deployment
1. Configure GCP project
2. Set environment variables
3. Run: `./scripts/deploy.sh`
4. Cloud Build handles build + deploy

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14, React, TypeScript | UI framework (strict mode disabled) |
| Styling | Tailwind CSS, Framer Motion | Sensory-friendly design + animations |
| Backend | FastAPI, Python 3.11 | Async WebSocket server |
| AI Models | Gemini 2.0 Flash, Imagen 3 | Voice, vision, image generation |
| Demo Mode | Demo Services (Python) | Simulated AI for testing without APIs |
| Database | Firestore | Session storage |
| Storage | Cloud Storage | Asset storage |
| Hosting | Cloud Run | Containerized deployment |
| Build | Docker, Cloud Build | CI/CD pipeline |

**Note**: React strict mode is disabled (`reactStrictMode: false`) to prevent WebSocket duplicate connections.

## Future Enhancements

1. **Video Generation**: Integrate Veo for 3-5s animated clips
2. **Parent Dashboard**: View child's daily stories
3. **Emotion Analytics**: Track emotional patterns over time
4. **Multi-language**: Support for multiple languages
5. **Offline Mode**: Local storage for areas with poor connectivity
