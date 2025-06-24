import schedule
import time
import asyncio
import aiosqlite
from datetime import datetime
from ctr.message import sendchatwork

async def reset_omikuji():
    async with aiosqlite.connect("omikuji.db") as db:
        await db.execute("DELETE FROM omikuji")
        await db.commit()
        print(f"{datetime.now()} おみくじリセット完了")

    date_str = datetime.now().strftime("%Y年%m月%d日")
    await send_chatwork_message(f"日付が変わりました！今日は {date_str} です")

def run_reset_job():
    asyncio.run(reset_omikuji())

schedule.every().day.at("00:00").do(run_reset_job)

print("スケジューラー起動中（毎日0時におみくじリセット）...")

while True:
    schedule.run_pending()
    time.sleep(30)
