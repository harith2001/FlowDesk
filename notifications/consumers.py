from __future__ import annotations

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer that streams notifications for the authenticated user.
    """

    async def connect(self):
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            await self.close()
            return

        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope.get("user")
        if getattr(self, "group_name", None) and user and not user.is_anonymous:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notification_message(self, event):
        """
        Handler for messages sent to the group.
        """

        await self.send_json(event["data"])

