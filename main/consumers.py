# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Car

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("likes_group", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("likes_group", self.channel_name)

    async def like_update(self, event):
        await self.send(text_data=json.dumps({
            'car_id': event['car_id'],
            'likes_count': event['likes_count'],
            'liked': event['liked']
        }))