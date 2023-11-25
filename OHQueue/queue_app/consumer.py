from channels.generic.websocket import AsyncWebsocketConsumer
import json

class QueueConsumer(AsyncWebsocketConsumer):
    joined_users = set()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if not user.is_anonymous and user.username in self.joined_users:
            self.joined_users.remove(user.username)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        name = text_data_json['name']  # Define 'name' here so it's accessible in both blocks

        # Join send back
        if action == 'join':            
            if name not in self.joined_users:
                self.joined_users.add(name)
                question = text_data_json.get('question', '')
                location = text_data_json.get('location', '')

                response = {
                    'action': 'join',
                    'name': name,
                    'question': question,
                    'location': location
                }
        
                # Send the response back to the client
                await self.send(text_data=json.dumps(response))

        # Leave send back
        elif action == 'leave' and name in self.joined_users:
            self.joined_users.remove(name)

            response = {
                'action': 'leave',
                'name': name
            }
            await self.send(text_data=json.dumps(response))
