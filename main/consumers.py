# main/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("likes", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("likes", self.channel_name)

    async def receive(self, text_data):
        pass  # Клиенты не отправляют сообщения

    async def like_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))