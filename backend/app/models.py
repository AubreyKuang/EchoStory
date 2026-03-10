"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class StorySegment(BaseModel):
    """A single story segment"""
    id: str
    text: str
    illustration_url: Optional[str] = None
    emotion: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Session(BaseModel):
    """A story session"""
    id: str
    created_at: str
    updated_at: str
    story_segments: List[StorySegment] = []
    status: str = "active"


class AudioChunkMessage(BaseModel):
    """Audio chunk WebSocket message"""
    type: str = "audio_chunk"
    data: str  # Base64 encoded audio
    is_final: bool = False


class VideoFrameMessage(BaseModel):
    """Video frame WebSocket message"""
    type: str = "video_frame"
    data: str  # Base64 encoded image


class TextInputMessage(BaseModel):
    """Text input WebSocket message"""
    type: str = "text_input"
    text: str


class InterruptMessage(BaseModel):
    """Interrupt WebSocket message"""
    type: str = "interrupt"


class GenerateIllustrationMessage(BaseModel):
    """Generate illustration WebSocket message"""
    type: str = "generate_illustration"
    description: str
    scene_type: Optional[str] = None


class SaveSegmentMessage(BaseModel):
    """Save segment WebSocket message"""
    type: str = "save_segment"
    segment: StorySegment
