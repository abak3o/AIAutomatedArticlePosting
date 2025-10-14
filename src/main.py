import schedule
import time
from article_poster import ArticlePoster
from discord import send_discord_log
from config import config

def scheduled_job():
    """スケジュール実行用のジョブ"""
    print(f"🕒 ジョブ実行開始: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        poster = ArticlePoster(config.LIVEDOOR_USER_ID, config.LIVEDOOR_USER_PASSWD)
        result = poster.run()
        
        if result['status'] == 'success':
            print(f"✅ 投稿成功: {result.get('title', '')}")
        else:
            print(f"⚠️ 投稿失敗: {result.get('message', '')}")
            
    except Exception as e:
        print(f"❌ 実行エラー: {e}")

# 30分ごとのスケジュール設定
schedule.every(30).minutes.do(scheduled_job)

if __name__ == "__main__":
    print("🕒 30分間隔スケジューラーを開始しました...")
    send_discord_log("🕒 30分間隔スケジューラーを開始しました...")
    print("⏰ 実行間隔: 30分ごと")
    print("🛑 Ctrl+Cで終了")
    
    # 初回実行（コメントアウト解除で有効化）
    print("🚀 初回実行します...")
    scheduled_job()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにチェック
    except KeyboardInterrupt:
        print("👋 スケジューラーを終了します")
