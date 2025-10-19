import json
import base64
from django.core.files.base import ContentFile
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.chat.models import Room, Message
from apps.accounts.models import CustomUser
import re

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room"]
        self.group_name = f"chat_{self.room_name}"


        # Nettoyage du nom pour être compatible Channels
        safe_room_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', self.room_name)
        self.group_name = f"chat_{safe_room_name}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"✅ Connecté à {self.group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data.get("message", "")
        username = data.get("username", "")
        image_data = data.get("image", None)

        msg_dict = await self._save_message(self.room_name, username, message, image_data)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "payload": msg_dict,
            }
        )

    async def chat_message(self, event):
        payload = event["payload"]
        await self.send(text_data=json.dumps(payload))

    @database_sync_to_async
    def _save_message(self, room_name, username, text, image_data=None):
        room = Room.objects.get(name__iexact=room_name)
        user = CustomUser.objects.filter(username=username).first()
        msg = Message.objects.create(user=user, room=room, value=text or "")

        if image_data:
            try:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                msg.image.save(
                    f"{username}_{msg.pk}.{ext}",
                    ContentFile(base64.b64decode(imgstr)),
                    save=True
                )
            except Exception as e:
                print("⚠️ Erreur décodage image :", e)

        return {
            "user": user.username if user else "Inconnu",
            "value": msg.value,
            "created": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "image": msg.image.url if msg.image else None,
        }
