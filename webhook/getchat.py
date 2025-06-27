from fastapi import APIRouter, Request
from modules.omikuji import omikuji
import requests
import os
import aiosqlite
import random

CHATWORK_TOKEN = os.getenv("CHATWORK_API_TOKEN")

class Chatwork:
    def _init_(self, api_key):
        self.api_url = 'https://api.chatwork.com/v2'
        self.headers = { 'X-ChatworkToken': api_key }

        async def parse_request(self):
            self.req = await request.json()
            self.data = self.req["webhook_event"]
            self.body = self.data.get("body")
            self.accountId = self.data.get("account_id")
            self.roomId = self.data.get("room_id")
            self.messageId = self.data.get("message_id")
            self.send_time = self.data.get("send_time")
            self.update_time = self.data.get("update_time")
            print(self.body)
            
        def command(self):
            if self.body == 'おみくじ':
                self.omikuji()

        def omikujiresult(self):
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
                    
        async def omikuji(self):
                name = await self.sendername()
                async with aiosqlite.connect("omikuji.db") as db:
                    db.row_factory = aiosqlite.Row
                    async with db.execute(
                        "SELECT * FROM omikuji WHERE accountId = ?", (self.accountId,)
                    ) as cursor:
                        existing = await cursor.fetchone()

                    if existing:
                        await sendmessage(f"[rp aid={self.accountId} to={self.room_id}-{self.message_id}] おみくじは1日1回までです。")
                        return {"status": "already_drawn"}

                    result = omikujiresult()
                    await db.execute(
                        "INSERT INTO omikuji (accountId, result, roomId, name) VALUES (?, ?, ?, ?)",
                        (self.accountId, result, self.roomId, self.name),
                    )
                    await db.commit()
                    await self.sendmessage(f"[rp aid={self.accountId} to={self.roomId}-{self.messageId}][pname:{self.accountId}] さん\n{result}")
                    return {"status": "ok", "result": result}
            
        def sendmessage(self, ms):
            try:
                response = requests.post(f'{self.api_url}/rooms/{self.roomId}/messages', data={"body": ms}, headers=self.headers)
                if response.status_code == 200:
                    print("メッセージを送信しました")
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"エラー: {e}")
        def sendername(self):
            try:
                response = requests.post(f"{self.api_url}/rooms/{self.roomId}/members", headers=self.headers)
                if response.status_code == 200:
                    print("名前を取得")
                    members = response.data
                    sender = next((m for m in members if m["account_id"] == self.accountId), None)
                    name = sender["name"] if sender else "名前を取得できませんでした"
                    return name
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"エラー: {e}")

router = APIRouter()

@router.post("/getchat")
async def getchat(request: Request):
    chatwork = Chatwork(CHATWORK_TOKEN)
    await chatwork.parse_request(request)
    await command()
