# main/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("likes_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("likes_group", self.channel_name)

    async def like_update(self, event):
        # Отправляем обновление всем клиентам
        await self.send(text_data=json.dumps({
            'car_id': event['car_id'],
            'likes_count': event['likes_count'],
            'user_has_liked': event.get('user_has_liked', False)
        }))