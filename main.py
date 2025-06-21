from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def send():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(request: Request):
    req_body = await request.json()
    data = req_body["webhook_event"]
    body = data.get("body")
    account_id = data.get("account_id")
    room_id = data.get("room_id")
    message_id = data.get("message_id")
    send_time = data.get("send_time")
    update_time = data.get("update_time")
    print(body)
