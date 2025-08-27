# requestsは別途インストールが必要です: pip install requests
import os
import requests
import time

# 環境変数を取得
API_TOKEN = os.environ.get("CHATWORK_API_TOKEN")
ROOM_ID = os.environ.get("ROOM_ID")

if not API_TOKEN or not ROOM_ID:
    print("エラー: 環境変数 'CHATWORK_API_TOKEN' と 'ROOM_ID' を設定してください。")
    exit()

def post_message():
    """requestsを使ってメッセージを投稿する関数"""
    try:
        url = f"https://api.chatwork.com/v2/rooms/{ROOM_ID}/messages"
        headers = {
            "X-ChatWorkToken": API_TOKEN
        }
        data = {
            "body": "あ"
        }

        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            print(f"メッセージを投稿しました: {response.json()}")
            time.sleep(1)
        elif response.status_code == 429:
            print("レート制限に達しました。5分間待機します...")
            time.sleep(300)
        else:
            print(f"エラーが発生しました: {response.status_code} - {response.text}")
            time.sleep(10)

    except requests.exceptions.RequestException as e:
        print(f"ネットワークエラーが発生しました: {e}")
        time.sleep(10)

if __name__ == "__main__":
    while True:
        post_message()
