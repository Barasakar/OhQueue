from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class QueueConsumer(AsyncWebsocketConsumer):
    online_tas = set()  # Set to keep track of online TAs
    queue_group_name = 'queue_group'

    async def queue_update(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def connect(self):
        await self.channel_layer.group_add(self.queue_group_name, self.channel_name)
        await self.accept()

        user = self.scope["user"]
        user_in_queue = await self.is_user_in_queue(user.username)
        await self.send(text_data=json.dumps({
            'action': 'user_status',
            'in_queue': user_in_queue
        }))

        if user.is_authenticated and user.role == 'TA':
            self.online_tas.add(user.username)
            await self.update_ta_list()

        await self.send_current_state()


    async def disconnect(self, close_code):
        user = self.scope["user"]
        await self.channel_layer.group_discard(self.queue_group_name, self.channel_name)

        # if user.username in self.joined_users:
        #     self.joined_users.remove(user.username)

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

    @sync_to_async
    def save_queue_entry(self, name, question, location):
        # Import the model inside the method
        from .models import QueueEntry
        QueueEntry.objects.create(name=name, question=question, location=location)

    @sync_to_async
    def remove_queue_entry(self, name):
        # Import the model inside the method
        from .models import QueueEntry
        QueueEntry.objects.filter(name=name).delete()

    @sync_to_async
    def get_all_queue_entries(self):
        # Import the model inside the method
        from .models import QueueEntry
        return list(QueueEntry.objects.values())
    
    @sync_to_async
    def is_user_in_queue(self, name):
        from .models import QueueEntry
        # return QueueEntry.objects.filter(name=name, in_queue=True).exists()
        QueueEntry.objects.filter(name=name).exists()

    async def send_current_state(self):
        queue_entries = await self.get_all_queue_entries()
        await self.send(text_data=json.dumps({
            'action': 'initial_state',
            'tas': list(self.online_tas),
            'queue': queue_entries
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        name = text_data_json['name']

        if action == 'join':
            if name not in self.online_tas:
                question = text_data_json.get('question', '')
                location = text_data_json.get('location', '')
                await self.save_queue_entry(name, question, location)

        elif action == 'leave':
            await self.remove_queue_entry(name)

        # After join or leave, get the updated queue and send it to all clients
        queue_entries = await self.get_all_queue_entries()
        await self.channel_layer.group_send(
            self.queue_group_name,
            {
                'type': 'queue_update',
                'message': {
                    'action': 'update_queue',
                    'queue': queue_entries
                }
            }
        )
