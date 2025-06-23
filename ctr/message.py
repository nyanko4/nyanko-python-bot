import requests
import os
from dotenv import load_dotenv

load_dotenv()
CHATWORK_TOKEN = os.getenv("CHATWORK_API_TOKEN")

def sendchatwork(ms, roomId):
    try:
        requests.post(
            f"https://api.chatwork.com/v2/rooms/{roomId}/messages", 
            data={
                "self_unread": 0,
                "body": ms
            },
            headers={
                "X-ChatWorkToken": CHATWORK_TOKEN,
                "content-type": "application/x-www-form-urlencoded"
                }
        )
        if response.status_code == 200:
            print("メッセージを送信しました")
        else:
            print(f"Chatwork送信失敗: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"ネットワークまたはリクエストエラー: {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")
