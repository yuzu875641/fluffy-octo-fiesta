import os
import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

# 環境変数からAPIトークンとルームIDを取得
API_TOKEN = os.environ.get("CHATWORK_API_TOKEN")
ROOM_ID = os.environ.get("ROOM_ID")

if not API_TOKEN or not ROOM_ID:
    # 環境変数が設定されていない場合でもアプリを起動
    print("警告: 環境変数 'CHATWORK_API_TOKEN' と 'ROOM_ID' が設定されていません。メッセージは投稿されません。")
else:
    # メッセージ投稿スレッドを開始
    def post_message_thread():
        while True:
            try:
                url = f"https://api.chatwork.com/v2/rooms/{ROOM_ID}/messages"
                headers = {"X-ChatWorkToken": API_TOKEN}
                data = {"body": "あ"}

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

    # バックグラウンドで投稿スレッドを開始
    import threading
    t = threading.Thread(target=post_message_thread, daemon=True)
    t.start()

@app.route('/')
def keep_alive():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
