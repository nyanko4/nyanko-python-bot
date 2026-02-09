from fastapi import FastAPI
from webhook.router import router as webhook_router
from cron.daily_task import start_daily_task

app = FastAPI(
    title="Chatwork Bot API",
    description="Chatwork Webhook + Command Dispatcher",
    version="1.0.0",
)

# Webhook ルート登録
app.include_router(webhook_router)

# 起動時イベント
@app.on_event("startup")
async def startup_event():
    start_daily_task()
    print("FastAPI server started")

# 動作確認用
@app.get("/health")
async def health_check():
    return {"status": "ok"}
