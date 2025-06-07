import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Получаем channel_layer явно
        self.channel_layer = get_channel_layer()

        logger.info(f"Connecting to channel layer: {self.channel_layer}")

        if self.channel_layer is None:
            logger.error("Channel layer is None in connect!")
        else:
            try:
                await self.channel_layer.group_add(
                    "likes_group",
                    self.channel_name
                )
                await self.accept()
                logger.info("WebSocket connection established")
            except Exception as e:
                logger.error(f"Error in group_add: {str(e)}")
                await self.close()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("likes_group", self.channel_name)

    async def like_update(self, event):
        # Отправляем обновление всем клиентам
        await self.send(text_data=json.dumps({
            'car_id': event['car_id'],
            'likes_count': event['likes_count'],
            'user_has_liked': event.get('user_has_liked', False)
        }))