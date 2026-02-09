from pydantic import BaseModel
from typing import Optional

class WebhookEvent(BaseModel):
    body: str
    account_id: int
    room_id: int
    message_id: int
    send_time: Optional[int] = None
    update_time: Optional[int] = None


class ChatworkWebhook(BaseModel):
    webhook_event: WebhookEvent
