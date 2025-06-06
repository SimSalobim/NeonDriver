# main/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import Car

class LikeConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.accept()
            self.channel_layer.group_add("likes_group", self.channel_name)
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            self.close()