from fastapi import APIRouter
import aiosqlite
import random
import re
from ctr.message import sendchatwork

def omikujiresult():
    probability = random.randint(1, 1000)
    if probability < 50:
        return "大凶"  # 5%
    elif probability < 250:
        return "小吉"  # 20%
    elif probability < 423:
        return "末吉"  # 17.3%
    elif probability < 623:
        return "吉"    # 20%
    elif probability < 773:
        return "中吉"  # 15%
    elif probability < 873:
        return "凶"    # 10%
    elif probability < 874:
        return "願い事叶えたるよ(できることだけ)"  # 0.1%
    else:
        return "大吉"  # 12.6%

async def omikuji(body, accountId, roomId, messageId):
    if re.fullmatch("おみくじ", body.strip()):
        async with aiosqlite.connect("omikuji.db") as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM omikuji WHERE accountId = ?", (accountId,)
            ) as cursor:
                existing = await cursor.fetchone()

            if existing:
                await send_chatwork(
                    f"[rp aid={account_id} to={room_id}-{message_id}] おみくじは1日1回までです。",
                    room_id,
                )
                return {"status": "already_drawn"}

            result = omikujiresult()
            await db.execute(
                "INSERT INTO omikuji (accoutId, result, roomId, name, date) VALUES (?, ?, ?, ?, ?)",
                (accountId, result, roomId, sendername, date),
            )
            await db.commit()
            sendchatwork(f"[rp aid={accountId} to={roomId}-{messageId}][pname:{accountId}] さん\n{result}", roomId)
            return {"status": "ok", "result": omikuji_result}
    return {"status": "ignored"}
