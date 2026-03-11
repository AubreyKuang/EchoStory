"""
Demo Service - 模拟Gemini响应，用于演示
"""
import asyncio
import random
import base64
import json


class DemoGeminiService:
    """模拟Gemini服务，用于演示"""

    def __init__(self):
        self.sessions = {}
        self.story_context = []

    async def process_audio_stream(self, audio_data: str, session_id: str, is_final: bool = False):
        """模拟音频处理"""
        await asyncio.sleep(0.3)  # 模拟网络延迟

        responses = [
            "That sounds wonderful! Tell me more about it.",
            "How exciting! What happened next?",
            "I can imagine that! What did you see?",
            "That's amazing! How did you feel?",
            "Wow! That must have been fun!",
        ]

        text = random.choice(responses)

        # 随机决定是否触发图片生成
        should_generate_image = random.random() > 0.6

        function_calls = []
        if should_generate_image:
            function_calls.append({
                "name": "generate_illustration",
                "args": {
                    "description": "A friendly colorful scene with a child playing in a park",
                    "scene_type": "location"
                }
            })

        return {
            "text": text,
            "function_calls": function_calls,
            "is_complete": is_final
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
        # 使用placeholder图片服务
        width = 800
        height = 600

        # 生成不同颜色的占位图
        colors = ["FFB6C1", "87CEEB", "98FB98", "FFD700", "DDA0DD"]
        color = random.choice(colors)

        # 使用via.placeholder.com或其他占位图服务
        image_url = f"https://via.placeholder.com/{width}x{height}/{color}/FFFFFF?text=Story+Scene"

        # 转换为base64格式
        return base64.b64encode(image_url.encode()).decode()
