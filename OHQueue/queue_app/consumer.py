from channels.generic.websocket import AsyncWebsocketConsumer
import json

class QueueConsumer(AsyncWebsocketConsumer):
    joined_users = set()
    queue_group_name = 'queue_group'

    async def queue_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def connect(self):
        await self.channel_layer.group_add(
            self.queue_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        await self.channel_layer.group_discard(
            self.queue_group_name,
            self.channel_name
        )
        if not user.is_anonymous and user.username in self.joined_users:
            self.joined_users.remove(user.username)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        name = text_data_json['name']

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
                await self.channel_layer.group_send(
                self.queue_group_name,
                {
                    'type': 'queue_update',
                    'message': response
                }
            )
                
        # Leave send back
        elif action == 'leave' and name in self.joined_users:
            self.joined_users.remove(name)

            response = {
                'action': 'leave',
                'name': name
            }
            await self.channel_layer.group_send(
                self.queue_group_name,
                {
                    'type': 'queue_update',
                    'message': response
                }
            )
