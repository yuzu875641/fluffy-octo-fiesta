import os
import time
import chatwork

# 環境変数からAPIトークンとルームIDを取得
API_TOKEN = os.environ.get("CHATWORK_API_TOKEN")
ROOM_ID = os.environ.get("ROOM_ID")

if not API_TOKEN or not ROOM_ID:
    print("Error: 環境変数 'CHATWORK_API_TOKEN' と 'ROOM_ID' を設定してください。")
    exit()

cw_client = chatwork.ChatworkClient(token=API_TOKEN)

def post_message():
    """メッセージを投稿し、レート制限の場合は待機する関数"""
    try:
        response = cw_client.post_messages(room_id=ROOM_ID, body="あ")
        print(f"メッセージを投稿しました: {response}")
        # 成功したら1秒待つ
        time.sleep(1)

    except chatwork.APIError as e:
        # ChatworkのAPIエラーを捕捉
        if e.status_code == 429:
            # レート制限 (429 Too Many Requests) の場合
            print("レート制限に達しました。解除されるまで待機します...")

            # レスポンスヘッダーからリセット時刻を取得
            # 注: python-chatworkライブラリがこのヘッダーをサポートしているか確認が必要です
            # この例ではシンプルに5分間待機する
            wait_time = 300  # 300秒 = 5分
            print(f"{wait_time}秒間、待機します。")
            time.sleep(wait_time)
            
        else:
            # その他のAPIエラー
            print(f"APIエラーが発生しました: {e.status_code} - {e.message}")
            time.sleep(10) # 別のエラーの場合は少し待って再試行

    except Exception as e:
        # その他のエラー
        print(f"予期せぬエラーが発生しました: {e}")
        time.sleep(10)

if __name__ == "__main__":
    while True:
        post_message()
