import hmac
import hashlib
import base64
import os
from webhook.schemas import ChatworkWebhook

WEBHOOK_TOKENS = [
    base64.b64decode(os.getenv("webhookTokenGetchat", "")),
    base64.b64decode(os.getenv("webhookTokenMention", "")),
]

def verify_signature(payload: ChatworkWebhook, signature: str | None) -> bool:
    # Chatwork の webhook 署名を検証する。

    if not signature:
        return False

    body_str = payload.model_dump_json(exclude_none=True)

    for token in WEBHOOK_TOKENS:
        if not token:
            continue

        h = hmac.new(token, body_str.encode("utf-8"), hashlib.sha256)
        expected = base64.b64encode(h.digest()).decode()

        if signature == expected:
            return True

    return False
