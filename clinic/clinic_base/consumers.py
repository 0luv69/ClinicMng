# messaging/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser

from django.db import close_old_connections
from asgiref.sync import sync_to_async

from account.models import Conversation, Message, Profile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        URL: ws://<host>/ws/chat/<conversation_id>/
        """
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.group_name = f"chat_{self.conversation_id}"

        # Check authentication and participation
        user = self.scope.get("user", None)
        if user is None or isinstance(user, AnonymousUser):
            # Reject unauthenticated
            await self.close(code=4001)
            return

        # Load profile and conversation in sync_to_async calls
        self.profile = await sync_to_async(Profile.objects.get)(user=user)
        try:
            self.conversation = await sync_to_async(Conversation.objects.get)(
                id=self.conversation_id
            )
        except Conversation.DoesNotExist:
            await self.close(code=4004)
            return

        # Verify that this profile is a participant
        is_participant = await sync_to_async(
            lambda: self.conversation.participants.filter(id=self.profile.id).exists()
        )()
        if not is_participant:
            await self.close(code=4003)
            return

        # All checks passed: join the group and accept the connection
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
        Expected JSON:
        {
            "type": "chat.message",           # optional, can use to route
            "content": "Hello, world!",
        }
        """
        if text_data is None:
            return

        data = json.loads(text_data)
        content = data.get("content", "").strip()
        if not content:
            return  # ignore empty messages

        # Save message into DB
        message_obj = await sync_to_async(Message.objects.create)(
            conversation=self.conversation,
            sender=self.profile,
            content=content,
            timestamp=timezone.now(),
            read=False,
        )

        # Build the broadcast payload
        payload = {
            "message_id": message_obj.id,
            "conversation_id": self.conversation_id,
            "sender_id": self.profile.id,
            "sender_name": self.profile.user.get_full_name(),
            "content": content,
            "timestamp": timezone.localtime(message_obj.timestamp).strftime(
                "%I:%M %p, %d %b %Y"
            ),
        }

        # Broadcast to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",   # will route to chat_message()
                "payload": payload,
            },
        )

    async def chat_message(self, event):
        """
        Handler for messages sent to the group.
        Simply forwards the JSON to WebSocket clients.
        """
        await self.send(text_data=json.dumps(event["payload"]))
