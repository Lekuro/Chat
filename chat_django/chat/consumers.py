# async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.color = self.random_color()
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        message = f'{self.user.username} joined this chat room'
        self.log_message(self.room_name, self.user, message)
        await self.send_message(message)

        await self.accept()

    async def disconnect(self, close_code):
        message = f'{self.user.username} left this chat room'
        self.log_message(self.room_name, self.user, message)
        await self.send_message(message)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket

    async def receive(self, text_data):
        # login the user to this session.
        await login(self.scope, self.user)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.log_message(self.room_name, self.user, message)
        # Send message to room group
        await self.send_message(message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': event['user'],
            'color': event['color'],
            'user_id': event['user_id'],
        }))

    async def send_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'color': self.color,
                'user_id': self.user.id
            },
        )

    def log_message(self, chat_room_id, user_name, message):
        with open(f'logs/chatroom_{chat_room_id}.log', 'a') as f:
            f.write(f'{datetime.datetime.now()}\t{user_name}\t{message}\n')

    def random_color(self):
        import random
        colors_list = {
            'aqua': "#00ffff",
            'azure': "#f0ffff",
            'beige': "#f5f5dc",
            'black': "#000000",
            'blue': "#0000ff",
            'brown': "#a52a2a",
            'cyan': "#00ffff",
            'darkblue': "#00008b",
            'darkcyan': "#008b8b",
            'darkgrey': "#a9a9a9",
            'darkgreen': "#006400",
            'darkkhaki': "#bdb76b",
            'darkmagenta': "#8b008b",
            'darkolivegreen': "#556b2f",
            'darkorange': "#ff8c00",
            'darkorchid': "#9932cc",
            'darkred': "#8b0000",
            'darksalmon': "#e9967a",
            'darkviolet': "#9400d3",
            'fuchsia': "#ff00ff",
            'gold': "#ffd700",
            'green': "#008000",
            'indigo': "#4b0082",
            'khaki': "#f0e68c",
            'lightblue': "#add8e6",
            'lightcyan': "#e0ffff",
            'lightgreen': "#90ee90",
            'lightgrey': "#d3d3d3",
            'lightpink': "#ffb6c1",
            'lightyellow': "#ffffe0",
            'lime': "#00ff00",
            'magenta': "#ff00ff",
            'maroon': "#800000",
            'navy': "#000080",
            'olive': "#808000",
            'orange': "#ffa500",
            'pink': "#ffc0cb",
            'purple': "#800080",
            'violet': "#800080",
            'red': "#ff0000",
            'silver': "#c0c0c0",
            'white': "#ffffff",
            'yellow': "#ffff00"
        }
        return random.choice(list(colors_list.values()))
