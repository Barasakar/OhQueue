from channels.generic.websocket import AsyncWebsocketConsumer
import json

class QueueConsumer(AsyncWebsocketConsumer):
    joined_users = set()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # Handle disconnection logic
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'join':
            name = text_data_json['name']
            
            if name not in self.joined_users:
                self.joined_users.add(name)
                question = text_data_json['question']
                location = text_data_json['location']

                response = {
                    'action': 'join',
                    'name': name,
                    'question': question,
                    'location': location
                }

                # Send the response back to the client
                await self.send(text_data=json.dumps(response))
