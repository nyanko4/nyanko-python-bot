import requests
import os

CHATWORK_TOKEN = os.getenv("CHATWORK_API_TOKEN")

def sendername(accoutId, roomId):
    try:
        response = requests.post(
            f"https://api.chatwork.com/v2/rooms/{roomId}/members", 
            headers={
                "X-ChatWorkToken": CHATWORK_TOKEN,
                "accept": "application/json"
                }
        )
        if response.status_code == 200:
            print("名前を取得")
            members = response.data
            sender = next((m for m in members if m["account_id"] == accountId), None)
            name = sender["name"] if sender else "名前を取得できませんでした"
            return name
        else:
            print(f"Chatworkメンバー取得失敗: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"ネットワークまたはリクエストエラー: {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")
