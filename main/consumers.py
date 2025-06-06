# main/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Car


class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("likes_group", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("likes_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        car_id = data['car_id']

        car = await Car.objects.aget(id=car_id)
        await self.send(text_data=json.dumps({
            'car_id': car_id,
            'likes_count': car.likes.count()
        }))

    async def like_update(self, event):
        # Отправляем обновление всем клиентам
        await self.send(text_data=json.dumps(event))