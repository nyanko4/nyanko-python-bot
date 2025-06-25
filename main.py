from fastapi import FastAPI, Request
import asyncio
import aiosqlite
import schedule
import time
from datetime import datetime
from threading import Thread
from webhook.getchat import router as getchat
from db._init_db import _init_db
from ctr.message import sendchatwork
from quiz.send = router as quiz

app = FastAPI()

async def reset_omikuji():
    async with aiosqlite.connect("omikuji.db") as db:
        await db.execute("DELETE FROM omikuji")
        await db.commit()
        print(f"[{datetime.now()}] おみくじリセット完了")

    date_str = datetime.now().strftime("%Y年%m月%d日")
    await sendchatwork(f"日付が変わりました！今日は {date_str} です", 402828190)

def run_reset_job():
    asyncio.run(reset_omikuji())

def scheduler_loop():
    schedule.every().day.at("00:00").do(run_reset_job)
    print("スケジューラー起動中（毎日0時におみくじリセット）")
    while True:
        schedule.run_pending()
        time.sleep(30)
    
@app.get("/")
def send():
    return {"status": "ok"}
    
@app.on_event("startup")
async def startup():
    await _init_db()
def start_scheduler():
    Thread(target=scheduler_loop, daemon=True).start()
    
app.include_router(getchat)

app.include_router(quiz)
