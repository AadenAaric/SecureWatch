import cv2
import numpy as np
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from AI.CAMERA import VideoCamera


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.camera = VideoCamera(0)  # Use the appropriate camera index or video file
        self.send_frames = True
        asyncio.create_task(self.send_video_frames())

    async def disconnect(self, close_code):
        self.send_frames = False
        self.camera.__del__()
        del self.camera

    async def send_video_frames(self):
        while self.send_frames:
            frame = await self.camera.get_frame()

            # Convert to base64 string
            frame_base64 = base64.b64encode(frame).decode('utf-8')
            await self.send(text_data=frame_base64)

            # Control frame rate
            await asyncio.sleep(0.1)  # Adjust sleep duration to control frame rate