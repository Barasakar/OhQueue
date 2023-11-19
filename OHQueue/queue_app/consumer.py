from channels.generic.websocket import AsyncWebsocketConsumer
import json

class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #TODO: add some logic to accept connection
        await self.accept()

    async def disconnect(self, close_code):
        #TODO: add some logic to disconnect
        pass

    # implement joining or leaving action here.
    async def receive(self, text_data):
        pass