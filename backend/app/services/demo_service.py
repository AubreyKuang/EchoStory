"""
Demo Service - 模拟Gemini响应，用于演示
"""
import asyncio
import random
import base64
import json
import logging

logger = logging.getLogger(__name__)


class DemoGeminiService:
    """模拟Gemini服务，用于演示"""

    def __init__(self):
        self.sessions = {}
        self.story_context = []

    async def process_audio_stream(self, audio_data: str, session_id: str, is_final: bool = False):
        """模拟音频处理"""
        # 只在is_final=true时才响应（避免频繁闪烁）
        if not is_final:
            return {
                "text": "",
                "function_calls": [],
                "is_complete": False
            }

        await asyncio.sleep(0.5)  # 模拟处理时间

        responses = [
            "That sounds wonderful! Tell me more about it.",
            "How exciting! What happened next?",
            "I can imagine that! What did you see?",
            "That's amazing! How did you feel?",
            "Wow! That must have been fun!",
        ]

        text = random.choice(responses)

        # 每次都生成图片（方便测试）
        function_calls = [{
            "name": "generate_illustration",
            "args": {
                "description": "A friendly colorful scene with a child playing in a park",
                "scene_type": "location"
            }
        }]

        return {
            "text": text,
            "function_calls": function_calls,
            "is_complete": True
        }

    async def analyze_video_frame(self, frame_data: str, session_id: str):
        """模拟视觉分析"""
        await asyncio.sleep(0.5)

        # 模拟检测到的物体
        possible_objects = [
            ["teddy bear", "toy"],
            ["book", "notebook"],
            ["pencil", "pen"],
            ["cup", "mug"],
            ["phone"],
        ]

        objects = random.choice(possible_objects)

        return {
            "objects_detected": objects,
            "description": f"I can see a {objects[0]} in the frame!"
        }

    async def process_text(self, text: str, session_id: str):
        """模拟文本处理"""
        await asyncio.sleep(0.2)

        responses = [
            "That's a great story! What else happened?",
            "I love hearing about your day! Tell me more.",
            "That sounds really interesting! What did you do next?",
        ]

        return {
            "text": random.choice(responses),
            "function_calls": []
        }

    async def interrupt_generation(self, session_id: str):
        """模拟中断"""
        pass

    async def generate_illustration(self, description: str, session_id: str):
        """返回占位图片URL"""
        await asyncio.sleep(0.5)  # 模拟生成时间

        # 80%概率返回test.png，20%返回占位图
        use_test_image = random.random() > 0.2

        # 总是返回test.png（避免placeholder加载问题）
        logger.info("📸 Using test.png")
        return "http://localhost:3000/test.png"
