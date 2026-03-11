"""
Main FastAPI application for EchoStory
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.config import get_settings
from app.websocket_handler import WebSocketManager

# 获取配置
settings = get_settings()

# 根据配置选择真实或Demo服务
if settings.DEMO_MODE:
    logger.info("🎭 Running in DEMO MODE - using simulated responses")
    from app.services.demo_service import DemoGeminiService as GeminiService
else:
    logger.info("Running with real Gemini API")
    from app.services.gemini_service import GeminiService
    from app.services.storage_service import StorageService
    from app.services.firestore_service import FirestoreService

# Initialize services
websocket_manager = WebSocketManager()
gemini_service = GeminiService()

# Storage和Firestore在demo模式下可选
if not settings.DEMO_MODE:
    storage_service = StorageService()
    firestore_service = FirestoreService()
else:
    # Demo模式使用模拟服务
    class DemoStorageService:
        async def upload_image(self, image_url, session_id, content_type="image/png"):
            return f"https://via.placeholder.com/800x600/87CEEB/FFFFFF?text=Demo+Image"

    class DemoFirestoreService:
        async def save_session(self, session_id, session_data=None):
            return {"session_id": session_id, "status": "saved"}
        async def get_session(self, session_id):
            return {"session_id": session_id, "story_segments": []}
        async def save_segment(self, session_id, segment):
            pass
        async def list_sessions(self, limit=10, offset=0):
            return []

    storage_service = DemoStorageService()
    firestore_service = DemoFirestoreService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    logger.info("Starting EchoStory backend...")
    yield
    logger.info("Shutting down EchoStory backend...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "gemini": "connected",
            "storage": "connected",
            "firestore": "connected"
        }
    }


@app.websocket("/ws/story")
async def websocket_story_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real-time story interaction
    Handles voice, vision, and live story generation
    """
    await websocket_manager.connect(websocket)

    try:
        logger.info("New WebSocket connection established")

        # Initialize session
        session_id = await websocket_manager.initialize_session(websocket)

        # Send welcome message
        await websocket.send_json({
            "type": "session_initialized",
            "session_id": session_id,
            "message": "Welcome to EchoStory! I'm ready to create stories with you."
        })

        # Main message loop
        while True:
            # Receive message from client
            message = await websocket.receive_json()

            logger.info(f"Received message type: {message.get('type')}")

            # Route message to appropriate handler
            await websocket_manager.handle_message(
                websocket=websocket,
                message=message,
                session_id=session_id,
                gemini_service=gemini_service,
                storage_service=storage_service,
                firestore_service=firestore_service
            )

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        websocket_manager.disconnect(websocket)

    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"An error occurred: {str(e)}"
            })
        except:
            pass
        finally:
            websocket_manager.disconnect(websocket)


@app.post("/api/sessions/{session_id}/save")
async def save_session(session_id: str):
    """Save the current story session"""
    try:
        result = await firestore_service.save_session(session_id)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error saving session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Retrieve a story session"""
    try:
        session_data = await firestore_service.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        return JSONResponse(content=session_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions")
async def list_sessions(limit: int = 10, offset: int = 0):
    """List all story sessions"""
    try:
        sessions = await firestore_service.list_sessions(limit=limit, offset=offset)
        return JSONResponse(content={"sessions": sessions})
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
