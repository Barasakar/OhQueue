from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from django.utils import timezone

class QueueConsumer(AsyncWebsocketConsumer):
    online_tas = set()  # Set to keep track of online TAs
    queue_group_name = 'queue_group'

    async def queue_update(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

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
            self.online_tas.remove(user.username) 
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
    def save_queue_entry(self, username, name, question, location):
        from .models import QueueEntry
        QueueEntry.objects.filter(username=username).delete()
        QueueEntry.objects.create(username=username, name=name, question=question, location=location, in_queue=True)

    @sync_to_async
    def remove_queue_entry(self, name):
        from .models import QueueEntry
        QueueEntry.objects.filter(name=name).update(in_queue=False, assisting_ta=None)

    @sync_to_async
    def get_all_queue_entries(self):
        from .models import QueueEntry
        entries = QueueEntry.objects.all()
        queue_entries = []
        for entry in entries:
            queue_entries.append({
                "username": entry.username,
                "name": entry.name,
                "question": entry.question,
                "location": entry.location,
                "in_queue": entry.in_queue,
                "creation_date": timezone.localtime(entry.creation_date).isoformat(),  # Convert datetime to string
                "assisting_ta": entry.assisting_ta
            })
        return queue_entries
    
    @sync_to_async
    def is_user_in_queue(self, name):
        from .models import QueueEntry
        try:
            queue_entry = QueueEntry.objects.get(name=name)
            return queue_entry.in_queue
        except QueueEntry.DoesNotExist:
            return False

    
    async def answer_queue_item(self, student_username, ta_username):
        await sync_to_async(self._update_queue_entry_assistance)(student_username, ta_username)
        message = {
            'action': 'answer',
            'studentUsername': student_username,
            'taUsername': ta_username
        }

        await self.channel_layer.group_send(
            self.queue_group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )

    def _update_queue_entry_assistance(self, student_username, ta_username):
        from .models import QueueEntry
        QueueEntry.objects.filter(username=student_username).update(assisting_ta=ta_username)



    async def send_current_state(self):
        queue_entries = await self.get_all_queue_entries()
        await self.update_ta_list()
        await self.send(text_data=json.dumps({
            'action': 'initial_state',
            'tas': list(self.online_tas),
            'queue': queue_entries
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        username = self.scope["user"].username

        if action == 'join':
            if username not in self.online_tas:
                question = text_data_json.get('question', '')
                location = text_data_json.get('location', '')
                await self.save_queue_entry(username, username, question, location)
        elif action == 'leave':
            await self.remove_queue_entry(username)
        
        if action == 'answer':
        # Handle the answer action
            student_username = text_data_json['studentUsername']
            await self.answer_queue_item(student_username, username)

        if action == 'delete':
            student_username = text_data_json['studentUsername']
            await self.remove_queue_entry(student_username)

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

