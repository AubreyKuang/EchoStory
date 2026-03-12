"""
WebSocket connection manager and message handler
"""
from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections and message routing"""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.sessions: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()

    def disconnect(self, websocket: WebSocket):
        """Remove a disconnected WebSocket"""
        session_id = None
        for sid, ws in self.active_connections.items():
            if ws == websocket:
                session_id = sid
                break

        if session_id:
            del self.active_connections[session_id]
            logger.info(f"Session {session_id} disconnected")

    async def initialize_session(self, websocket: WebSocket) -> str:
        """Initialize a new story session"""
        session_id = str(uuid.uuid4())
        self.active_connections[session_id] = websocket
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "story_segments": [],
            "current_context": "",
            "is_generating": False
        }
        return session_id

    async def handle_message(
        self,
        websocket: WebSocket,
        message: dict,
        session_id: str,
        gemini_service,
        storage_service,
        firestore_service
    ):
        """Route incoming messages to appropriate handlers"""
        message_type = message.get("type")

        handlers = {
            "audio_chunk": self._handle_audio_chunk,
            "video_frame": self._handle_video_frame,
            "text_input": self._handle_text_input,
            "interrupt": self._handle_interrupt,
            "generate_illustration": self._handle_generate_illustration,
            "save_segment": self._handle_save_segment,
        }

        handler = handlers.get(message_type)
        if handler:
            await handler(
                websocket=websocket,
                message=message,
                session_id=session_id,
                gemini_service=gemini_service,
                storage_service=storage_service,
                firestore_service=firestore_service
            )
        else:
            logger.warning(f"Unknown message type: {message_type}")
            await websocket.send_json({
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            })

    async def _handle_audio_chunk(self, websocket, message, session_id, gemini_service, **kwargs):
        """Handle incoming audio chunks for real-time speech processing"""
        try:
            audio_data = message.get("data")  # Base64 encoded audio
            is_final = message.get("is_final", False)
            storage_service = kwargs.get("storage_service")

            logger.info(f"🎤 Processing audio chunk (final={is_final})")

            # Process audio with Gemini Live API
            response = await gemini_service.process_audio_stream(
                audio_data=audio_data,
                session_id=session_id,
                is_final=is_final
            )

            # 只在有实际内容时发送响应
            has_text = response.get("text") and response.get("text").strip()
            has_calls = response.get("function_calls") and len(response.get("function_calls", [])) > 0

            if has_text or has_calls:
                logger.info(f"📤 Sending audio response: text={bool(has_text)}, calls={bool(has_calls)}")
                # Send response back to client
                await websocket.send_json({
                    "type": "audio_response",
                    "data": response
                })

                # Process function calls (e.g., generate illustrations)
                if has_calls:
                    for fc in response["function_calls"]:
                        if fc["name"] == "generate_illustration":
                            logger.info(f"🎨 Generating illustration...")

                            try:
                                # Generate illustration
                                image_url = await gemini_service.generate_illustration(
                                    description=fc["args"].get("description", "A story scene"),
                                    session_id=session_id
                                )

                                logger.info(f"📸 Generated image URL: {image_url}")

                                # Upload to storage (in demo mode this is a no-op)
                                if storage_service:
                                    stored_url = await storage_service.upload_image(
                                        image_url=image_url,
                                        session_id=session_id
                                    )
                                else:
                                    stored_url = image_url

                                # Send image to client
                                await websocket.send_json({
                                    "type": "illustration_generated",
                                    "url": stored_url,
                                    "description": fc["args"].get("description", "")
                                })

                                logger.info(f"✅ Illustration sent: {stored_url}")
                            except Exception as img_error:
                                logger.error(f"❌ Error generating illustration: {str(img_error)}", exc_info=True)
            else:
                logger.debug(f"⏭️ Skipping empty response")

        except Exception as e:
            logger.error(f"❌ Error handling audio chunk: {str(e)}", exc_info=True)
            try:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Audio processing error: {str(e)}"
                })
            except:
                pass

    async def _handle_video_frame(self, websocket, message, session_id, gemini_service, **kwargs):
        """Handle incoming video frames for Live Vision"""
        try:
            frame_data = message.get("data")  # Base64 encoded image
            logger.debug(f"📹 Processing video frame")

            # Analyze frame with Gemini Vision
            analysis = await gemini_service.analyze_video_frame(
                frame_data=frame_data,
                session_id=session_id
            )

            # Always send vision detection result (even if empty)
            # This ensures frontend clears old tags when no objects are detected
            objects = analysis.get("objects_detected", [])
            if len(objects) > 0:
                logger.info(f"👀 Objects detected: {objects}")
            else:
                logger.debug(f"👀 No objects detected (warmup or clear frame)")

            await websocket.send_json({
                "type": "vision_detection",
                "data": analysis
            })

        except Exception as e:
            logger.error(f"❌ Error handling video frame: {str(e)}", exc_info=True)

    async def _handle_text_input(self, websocket, message, session_id, gemini_service, **kwargs):
        """Handle text input from user"""
        try:
            text = message.get("text", "")

            # Process with Gemini
            response = await gemini_service.process_text(
                text=text,
                session_id=session_id
            )

            # Send response
            await websocket.send_json({
                "type": "text_response",
                "data": response
            })

        except Exception as e:
            logger.error(f"Error handling text input: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "message": f"Text processing error: {str(e)}"
            })

    async def _handle_interrupt(self, websocket, message, session_id, gemini_service, **kwargs):
        """Handle user interruption of AI response"""
        try:
            # Stop current generation
            await gemini_service.interrupt_generation(session_id)

            # Mark session as not generating
            if session_id in self.sessions:
                self.sessions[session_id]["is_generating"] = False

            await websocket.send_json({
                "type": "interrupted",
                "message": "Generation stopped"
            })

        except Exception as e:
            logger.error(f"Error handling interrupt: {str(e)}")

    async def _handle_generate_illustration(
        self, websocket, message, session_id, gemini_service, storage_service, **kwargs
    ):
        """Handle illustration generation request (Tool Call)"""
        try:
            description = message.get("description", "")

            # Generate image with Imagen 3
            image_url = await gemini_service.generate_illustration(
                description=description,
                session_id=session_id
            )

            # Upload to Cloud Storage
            stored_url = await storage_service.upload_image(
                image_url=image_url,
                session_id=session_id
            )

            # Send image URL to client
            await websocket.send_json({
                "type": "illustration_generated",
                "url": stored_url,
                "description": description
            })

        except Exception as e:
            logger.error(f"Error generating illustration: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "message": f"Illustration generation error: {str(e)}"
            })

    async def _handle_save_segment(
        self, websocket, message, session_id, firestore_service, **kwargs
    ):
        """Save a story segment to Firestore"""
        try:
            segment = message.get("segment")

            # Add to session
            if session_id in self.sessions:
                self.sessions[session_id]["story_segments"].append(segment)

            # Save to Firestore
            await firestore_service.save_segment(session_id, segment)

            await websocket.send_json({
                "type": "segment_saved",
                "segment_id": segment.get("id")
            })

        except Exception as e:
            logger.error(f"Error saving segment: {str(e)}")
