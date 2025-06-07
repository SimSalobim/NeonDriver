import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.channel_layer = get_channel_layer()
            if self.channel_layer is None:
                logger.error("Channel layer is None in connect!")
                await self.close()
                return

            logger.info(f"Connecting to channel layer: {self.channel_layer}")

            await self.channel_layer.group_add(
                "likes_group",
                self.channel_name
            )
            await self.accept()
            logger.info("WebSocket connection established")

        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            await self.close()

    async def disconnect(self, close_code):
        try:
            if hasattr(self, 'channel_layer') and self.channel_layer:
                await self.channel_layer.group_discard(
                    "likes_group",
                    self.channel_name
                )
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

    async def like_update(self, event):
        # Отправляем обновление всем клиентам
        await self.send(text_data=json.dumps({
            'car_id': event['car_id'],
            'likes_count': event['likes_count'],
            'user_has_liked': event.get('user_has_liked', False)
        }))