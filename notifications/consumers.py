import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import asyncio
from video_streams.views import camera_instances
from AI.detector import *
from asgiref.sync import async_to_sync
# shared_middlewares/authentication.py


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()
        
        self.prediction_task = asyncio.create_task(self.send_predictions())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)
        self.prediction_task.cancel()

    async def receive(self, text_data):
        # Handle received messages here if needed
        pass
    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def send_predictions(self):
        await asyncio.sleep(1)
