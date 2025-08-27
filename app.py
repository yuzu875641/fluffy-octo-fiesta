import os
import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

# 環境変数からAPIトークンとルームIDを取得
API_TOKEN = os.environ.get("CHATWORK_API_TOKEN")
ROOM_ID = os.environ.get("ROOM_ID")

def post_message():
    """メッセージを投稿し、レート制限の場合は待機する関数"""
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
            time.sleep(1) # 1秒待機
        elif response.status_code == 429:
            print("レート制限に達しました。5分間待機します...")
            time.sleep(300) # 5分間待機
        else:
            print(f"エラーが発生しました: {response.status_code} - {response.text}")
            time.sleep(10)
    
    except requests.exceptions.RequestException as e:
        print(f"ネットワークエラーが発生しました: {e}")
        time.sleep(10)

def bot_loop():
    """ボットのメインループ"""
    # APIトークンとルームIDが設定されているか確認
    if not API_TOKEN or not ROOM_ID:
        print("警告: 環境変数が設定されていません。メッセージは投稿されません。")
        return

    while True:
        post_message()

@app.route('/')
def keep_alive():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Botのループを別のスレッドで実行
    import threading
    t = threading.Thread(target=bot_loop, daemon=True)
    t.start()

    # Flaskアプリを起動して、Renderのヘルスチェックに応答する
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
