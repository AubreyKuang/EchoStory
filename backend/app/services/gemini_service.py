"""
Gemini Live API Service for real-time multimodal interaction
"""
import google.generativeai as genai
from google.cloud import aiplatform
import asyncio
import logging
import base64
import json
from typing import Dict, Optional, AsyncGenerator
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:
    """Service for interacting with Gemini Live API"""

    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.active_streams: Dict[str, bool] = {}

        # Initialize Vertex AI for Imagen
        aiplatform.init(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.VERTEX_AI_LOCATION
        )

        # System instructions for the Gentle Playmate persona
        self.system_instruction = """
You are a gentle, patient AI companion helping autistic children tell stories about their day.

Core Principles:
1. LOW-DEMAND: Never pressure the child to speak. Accept any input (words, sounds, gestures).
2. VALIDATION: Every contribution is valuable. Celebrate and build on what they share.
3. SCAFFOLDING: Offer gentle prompts and choices, not open-ended questions.
4. VISUAL-FIRST: When you describe scenes, be concrete and visual.
5. EMOTION LABELING: Help identify and name emotions gently.

Communication Style:
- Use simple, short sentences (5-10 words)
- Speak slowly and clearly
- Offer choices: "Was it fun or quiet?" not "How did you feel?"
- Validate immediately: "I hear you!" "That's interesting!"
- Never correct or judge

Story Building:
- When the child shares something, immediately acknowledge it
- Build on their input: "A dog! What color is the dog?"
- If they change the story, embrace it: "Oh, now it's blue! I love blue dogs!"
- Use function calling to trigger illustrations at key moments

Interruption Handling:
- If interrupted, IMMEDIATELY stop and listen
- Acknowledge the new input: "Oh! Tell me more about that!"
- Seamlessly incorporate the change into the story

Safety:
- All content must be child-safe and appropriate
- Avoid scary, violent, or overly complex themes
- Keep stories positive and empowering
"""

    def _get_model(self):
        """Get configured Gemini model"""
        return genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction=self.system_instruction,
            tools=[self._get_tool_definitions()],
            generation_config={
                "temperature": 0.9,
                "top_p": 0.95,
                "max_output_tokens": 1024,
            },
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]
        )

    def _get_tool_definitions(self):
        """Define tools for function calling"""
        return {
            "function_declarations": [
                {
                    "name": "generate_illustration",
                    "description": "Generate an illustration for the current story scene. Call this when describing a new location, character, or important moment.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Detailed visual description of the scene to illustrate (e.g., 'A friendly blue dog playing in a sunny park with green grass and colorful flowers')"
                            },
                            "scene_type": {
                                "type": "string",
                                "enum": ["character", "location", "action", "emotion"],
                                "description": "Type of scene being illustrated"
                            }
                        },
                        "required": ["description"]
                    }
                },
                {
                    "name": "save_story_segment",
                    "description": "Save the current story segment with text and emotion context",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The story text to save"
                            },
                            "emotion": {
                                "type": "string",
                                "enum": ["happy", "excited", "calm", "worried", "sad", "neutral"],
                                "description": "Detected emotion in this segment"
                            }
                        },
                        "required": ["text"]
                    }
                }
            ]
        }

    async def process_audio_stream(
        self,
        audio_data: str,
        session_id: str,
        is_final: bool = False
    ) -> dict:
        """Process audio stream with Gemini Live API"""
        try:
            # Initialize session if needed
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "chat": self._get_model().start_chat(history=[]),
                    "context": []
                }

            # Decode audio data
            audio_bytes = base64.b64decode(audio_data)

            # Send audio to Gemini
            chat = self.sessions[session_id]["chat"]
            self.active_streams[session_id] = True

            # Create multimodal prompt
            response = await asyncio.to_thread(
                chat.send_message,
                [
                    {"mime_type": "audio/wav", "data": audio_bytes},
                    "Listen to what the child is sharing and respond warmly."
                ],
                stream=True
            )

            # Collect response
            full_text = ""
            function_calls = []

            for chunk in response:
                if not self.active_streams.get(session_id, False):
                    # Interrupted
                    break

                if chunk.text:
                    full_text += chunk.text

                # Check for function calls
                if hasattr(chunk, 'function_calls'):
                    for fc in chunk.function_calls:
                        function_calls.append({
                            "name": fc.name,
                            "args": dict(fc.args)
                        })

            return {
                "text": full_text,
                "function_calls": function_calls,
                "is_complete": is_final
            }

        except Exception as e:
            logger.error(f"Error processing audio: {str(e)}")
            raise

    async def analyze_video_frame(self, frame_data: str, session_id: str) -> dict:
        """Analyze video frame for object detection (Live Vision)"""
        try:
            # Decode frame
            image_bytes = base64.b64decode(frame_data)

            # Use Gemini Vision
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            prompt = """
Look at this image. If you see any toys, objects, or interesting things, describe them briefly.
Format: {"objects_detected": ["object1", "object2"], "description": "brief description"}
"""

            response = await asyncio.to_thread(
                model.generate_content,
                [
                    {"mime_type": "image/jpeg", "data": image_bytes},
                    prompt
                ]
            )

            # Parse response
            try:
                result = json.loads(response.text)
            except:
                result = {
                    "objects_detected": [],
                    "description": response.text
                }

            return result

        except Exception as e:
            logger.error(f"Error analyzing frame: {str(e)}")
            return {"objects_detected": [], "description": ""}

    async def process_text(self, text: str, session_id: str) -> dict:
        """Process text input"""
        try:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "chat": self._get_model().start_chat(history=[]),
                    "context": []
                }

            chat = self.sessions[session_id]["chat"]

            response = await asyncio.to_thread(
                chat.send_message,
                text
            )

            return {
                "text": response.text,
                "function_calls": []
            }

        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            raise

    async def interrupt_generation(self, session_id: str):
        """Stop current generation for a session"""
        self.active_streams[session_id] = False
        logger.info(f"Generation interrupted for session {session_id}")

    async def generate_illustration(self, description: str, session_id: str) -> str:
        """Generate illustration using Imagen 3 via Vertex AI"""
        try:
            # Enhance prompt for child-friendly style
            enhanced_prompt = f"""
Children's book illustration style, warm and friendly, soft colors, simple shapes:
{description}

Style: Digital illustration, storybook art, gentle and inviting, no text, safe for children
"""

            # Use Vertex AI Imagen
            model = aiplatform.ImageGenerationModel.from_pretrained(settings.IMAGEN_MODEL)

            response = await asyncio.to_thread(
                model.generate_images,
                prompt=enhanced_prompt,
                number_of_images=1,
                aspect_ratio="1:1",
                safety_filter_level="block_most",
                person_generation="allow_adult"
            )

            # Get image URL or bytes
            if response.images:
                image = response.images[0]
                # Save to temporary location or return bytes
                return image._as_base64_string()

            raise Exception("No image generated")

        except Exception as e:
            logger.error(f"Error generating illustration: {str(e)}")
            raise
