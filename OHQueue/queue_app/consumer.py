from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class QueueConsumer(AsyncWebsocketConsumer):
    online_tas = set()  # Set to keep track of online TAs
    joined_users = set()
    user_queue = []    # this is for preserving all the current information.
    queue_group_name = 'queue_group'

    async def queue_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def connect(self):
        await self.channel_layer.group_add(self.queue_group_name, self.channel_name)
        await self.accept()

        user = self.scope["user"]
        if user.is_authenticated and user.role == 'TA':
            self.online_tas.add(user.username)  # Add TA to online TAs set
            await self.update_ta_list()
        await self.send_current_state()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        await self.channel_layer.group_discard(self.queue_group_name, self.channel_name)

        if user.username in self.joined_users:
            self.joined_users.remove(user.username)

        if user.is_authenticated and user.role == 'TA':
            self.online_tas.remove(user.username)  # Remove TA from online TAs set
            await self.update_ta_list()

    async def update_ta_list(self):
        # Broadcast updated TA list
        await self.channel_layer.group_send(
            self.queue_group_name, 
            {
                "type": "ta_list_update",
                "tas": list(self.online_tas)
            }
        )

    async def ta_list_update(self, event):
        # Send the updated TA list to the client
        await self.send(text_data=json.dumps({
            'action': 'update_ta_list',
            'tas': event['tas']
        }))

    async def send_current_state(self):
        print("Sending initial state, queue:", self.user_queue)
        await self.send(text_data=json.dumps({
        'action': 'initial_state',
        'tas': list(self.online_tas),
        'queue': self.user_queue
    }))

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

                self.user_queue.append({
                'name': name,
                'question': question,
                'location': location
                })

                response = {
                    'action': 'join',
                    'name': name,
                    'question': question,
                    'location': location
                }
                print("Updated user_queue after join:", self.user_queue)
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
            self.user_queue = [user for user in self.user_queue if user['name'] != name]
            print("Updated user_queue after leave:", self.user_queue)
            await self.channel_layer.group_send(
                self.queue_group_name,
                {
                    "type": "queue_update",
                    "message": {
                        "action": "update_queue",
                        "queue": self.user_queue
                    }
                }
            )
