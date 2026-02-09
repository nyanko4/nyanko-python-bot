from fastapi import APIRouter, Header, HTTPException
from webhook.schemas import ChatworkWebhook
from webhook.signature import verify_signature
from webhook.dispatcher import handle_webhook

router = APIRouter(tags=["webhook"])

@router.post("/getchat")
async def getchat(
    payload: ChatworkWebhook,
    signature: str = Header(None, alias="x-chatworkwebhooksignature")
):
    
    if not verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    await handle_webhook(payload, webhook_type="getchat")
    return {"status": "ok"}


@router.post("/mention")
async def mention(
    payload: ChatworkWebhook,
    signature: str = Header(None, alias="x-chatworkwebhooksignature")
):
    if not verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    await handle_webhook(payload, webhook_type="mention")
    return {"status": "ok"}
