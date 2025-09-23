import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Discord Webhook設定
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_log(message: str) -> None:
    if not DISCORD_WEBHOOK_URL:
        return
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=5)
    except:
        pass  # エラーは無視
