"""
Demo Service - Simulates Gemini responses for demonstration
Progressive story generation: sunshine → grassland → puppy
"""
import asyncio
import logging

logger = logging.getLogger(__name__)


class DemoGeminiService:
    """Demo service simulating Gemini for realistic presentation"""

    def __init__(self):
        self.sessions = {}
        self.story_stages = [
            {
                "text": "Oh, what a beautiful sunny day! The sun is shining so bright. Tell me, what do you see?",
                "image": "http://localhost:3000/test.png",
                "description": "A bright sunny sky with warm golden sunlight",
                "scene": "sunshine"
            },
            {
                "text": "I love it! The grass looks so soft and green. What a wonderful place to play! What did you do there?",
                "image": "http://localhost:3000/test2.png",
                "description": "A lush green meadow with soft grass under the warm sun",
                "scene": "grassland"
            },
            {
                "text": "Wow! A friendly puppy! Look at that happy face! Is the puppy playing with you?",
                "image": "http://localhost:3000/test3.png",
                "description": "A cute happy puppy playing on the green grass in the sunshine",
                "scene": "puppy"
            }
        ]

        # Vision detection objects - rotate slowly
        self.vision_objects = [
            {"objects": ["pen"], "description": "I can see a pen!"},
            {"objects": ["toy"], "description": "Oh, what a nice toy!"},
            {"objects": ["iphone", "phone"], "description": "I see your phone there!"},
        ]

    async def process_audio_stream(self, audio_data: str, session_id: str, is_final: bool = False):
        """Simulate audio processing with progressive story"""
        # Only respond when recording is complete (prevents UI flashing)
        if not is_final:
            return {
                "text": "",
                "function_calls": [],
                "is_complete": False
            }

        await asyncio.sleep(0.8)  # Realistic processing time

        # Initialize session state
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "interaction_count": 0,
                "vision_index": 0
            }

        session = self.sessions[session_id]
        stage_index = session["interaction_count"] % len(self.story_stages)
        stage = self.story_stages[stage_index]

        # Increment for next interaction
        session["interaction_count"] += 1

        logger.info(f"📖 Demo Story Stage {stage_index + 1}: {stage['scene']}")

        # Always generate illustration for demo
        function_calls = [{
            "name": "generate_illustration",
            "args": {
                "description": stage["description"],
                "scene_type": "location"
            }
        }]

        return {
            "text": stage["text"],
            "function_calls": function_calls,
            "is_complete": True
        }

    async def analyze_video_frame(self, frame_data: str, session_id: str):
        """Simulate vision analysis with realistic object detection"""
        await asyncio.sleep(0.6)

        # Initialize session if needed
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "interaction_count": 0,
                "vision_index": 0,
                "vision_call_count": 0  # Track vision API calls separately
            }

        session = self.sessions[session_id]

        # Ensure vision_call_count exists (in case session was created by audio first)
        if "vision_call_count" not in session:
            session["vision_call_count"] = 0

        session["vision_call_count"] += 1

        call_count = session["vision_call_count"]

        # Realistic detection timeline (assuming 3s per frame):
        # Call 1 (0-3s): Nothing detected - camera just starting
        # Calls 2-3 (3-9s): Pen detected
        # Calls 4-5 (9-15s): Toy detected
        # Calls 6-7 (15-21s): iPhone detected
        # Then repeat cycle

        if call_count <= 1:
            # Initial phase - no detection yet
            logger.info(f"👁️ Vision call {call_count}: Warming up, no objects detected")
            return {
                "objects_detected": [],
                "description": ""
            }

        # Calculate which object to show (changes every 2 frames after warmup)
        object_index = ((call_count - 2) // 2) % len(self.vision_objects)
        vision_data = self.vision_objects[object_index]

        logger.info(f"👁️ Vision call {call_count}: Detected {vision_data['objects']}")

        return {
            "objects_detected": vision_data["objects"],
            "description": vision_data["description"]
        }

    async def process_text(self, text: str, session_id: str):
        """Simulate text processing"""
        await asyncio.sleep(0.3)

        return {
            "text": "That sounds wonderful! Keep telling me more about your story.",
            "function_calls": []
        }

    async def interrupt_generation(self, session_id: str):
        """Simulate interruption"""
        logger.info(f"⏸️ Demo: Generation interrupted for {session_id}")

    async def generate_illustration(self, description: str, session_id: str):
        """Return progressive illustration URLs with realistic delay"""
        # Simulate realistic image generation time (increased for better demo effect)
        # This creates a nice "pending" period where frontend shows "Creating magic..."
        await asyncio.sleep(3.5)  # 3.5 seconds - realistic AI image generation time

        # Get current stage
        if session_id not in self.sessions:
            return "http://localhost:3000/test.png"

        session = self.sessions[session_id]
        # Use previous interaction count since it was incremented after stage selection
        stage_index = (session["interaction_count"] - 1) % len(self.story_stages)
        image_url = self.story_stages[stage_index]["image"]

        logger.info(f"🎨 Illustration ready after generation: {image_url}")
        return image_url
