from fastapi import APIRouter, Request
from modules.omikuji import omikuji

router = APIRouter()

@router.post("/getchat")
async def getchat(request: Request):
    req_body = await request.json()
    data = req_body["webhook_event"]
    body = data.get("body")
    accountId = data.get("account_id")
    roomId = data.get("room_id")
    messageId = data.get("message_id")
    send_time = data.get("send_time")
    update_time = data.get("update_time")
    print(body)
    modules = [omikuji]

    for module in modules:
        result = await module(body, accountId, roomId, messageId)
        if result == "ok":
            return { "ok": True }
        return { "ok": True }
