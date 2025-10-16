import os
import sys
from dotenv import load_dotenv

if len(sys.argv) < 2:
    sys.exit(1)
    
env_suffix = sys.argv[1]
dotenv_file = f".env.{env_suffix}"

load_dotenv(dotenv_path=dotenv_file)


class Config:

    MODE = os.getenv("MODE")

    # 禁止ワード
    forbidden_keywords = os.getenv("FORBIDDEN_KEYWORDS")
    if forbidden_keywords:
        FORBIDDEN_KEYWORDS = forbidden_keywords.split(",")
    else:
        FORBIDDEN_KEYWORDS = []

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
    GEMINI_MODEL = os.getenv("GEMINI_MODEL")

    # Discord設定
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    # アプリケーション設定
    VIEWPORT = {"width": 1920, "height": 1000}
    WAIT_TIMEOUT = 30000  # 30秒に延長
    POST_INTERVAL = 30  # 30秒に延長
    if MODE == "GAME":
        POST_INTERVAL = 60

    # 実行モード
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

config = Config()
