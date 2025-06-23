from fastapi import FastAPI, Request
from webhook.getchat import router as getchat

app = FastAPI()

@app.get("/")
def send():
    return {"status": "ok"}

app.include_router(getchat)
