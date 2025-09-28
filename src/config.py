import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Livedoorブログ設定
    LIVEDOOR_URL = os.getenv("LIVEDOOR_URL")
    LIVEDOOR_USER_ID = os.getenv("LIVEDOOR_USER_ID")
    LIVEDOOR_USER_PASSWD = os.getenv("LIVEDOOR_USER_PASSWD")

    # AI設定
    PROMPT = os.getenv("PROMPT")
    INSTRUCTIONS = os.getenv("INSTRUCTIONS")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

    # Discord設定
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    # アプリケーション設定
    VIEWPORT = {"width": 1920, "height": 1000}
    WAIT_TIMEOUT = 30000  # 30秒に延長

    # 実行モード
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

    # スケジュール設定
    SCHEDULE_TIMES = [
        "00:00",
        "07:00",
        "12:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
        "23:00",
    ]
    TEST_INTERVAL_MINUTES = 3  # テスト用インターバル


config = Config()
