from fastapi import APIRouter, Request
import httpx
import os
import random
import tracemalloc
tracemalloc.start()

CHATWORK_TOKEN = os.getenv("CHATWORK_API_TOKEN")

class Chatwork:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("CHATWORK_API_TOKENが設定されていません")
        self.api_url = 'https://api.chatwork.com/v2'
        self.headers = { 'X-ChatworkToken': api_key }

    async def parse_request(self, request):
        self.req = await request.json()
        self.data = self.req["webhook_event"]
        self.body = self.data.get("body")
        self.accountId = self.data.get("account_id")
        self.roomId = self.data.get("room_id")
        self.messageId = self.data.get("message_id")
        self.send_time = self.data.get("send_time")
        self.update_time = self.data.get("update_time")
        print(self.body)
            
    async def command(self):
        commands = {
            "おみくじ": self.omikuji()
        }
        handler = commands.get(self.body)
        if handler:
            await handler()
        else:
            print(f"commandに登録されていません {self.body}")
            
    async def getOmikujiResult(self):
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
        name = await self.senderName()
        omikujResult = await self.getOmikujiResult()
        await self.sendMessage(f"[rp aid={self.accountId} to={self.roomId}-{self.accountId}]{name}さん\n{omikujiResult}")
                
    async def sendMessage(self, ms):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f'{self.api_url}/rooms/{self.roomId}/messages', data={"body": ms}, headers=self.headers)
                response.raise_for_status()
                print("メッセージを送信しました")
        except httpx.HTTPStatusError as e:
            print(f"HTTPエラー: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"通信エラー: {e}")
            
    async def senderName(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/rooms/{self.roomId}/members", headers=self.headers)
                response.raise_for_status()
                print("名前を取得")
                members = response.json()
                sender = next((m for m in members if m["account_id"] == self.accountId), None)
                name = sender["name"] if sender else f"[pname:{self.accountId}]"
                return name
        except httpx.HTTPStatusError as e:
            print(f"HTTPエラー: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"通信エラー: {e}")
            
router = APIRouter()

@router.post("/getchat")
async def getchat(request: Request):
    chatwork = Chatwork(CHATWORK_TOKEN)
    await chatwork.parse_request(request)
    await chatwork.command()
