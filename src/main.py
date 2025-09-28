import os
import time
import logging
import schedule
from config import config
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright
from ai import chatGPT, gemini, deepseek
from thread2html import thread2html
from discord import send_discord_log

# ログ設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# 環境変数読み込み
load_dotenv()

def login(page):
    """ログイン処理"""
    try:
        page.goto(config.LIVEDOOR_URL)
        page.get_by_role("textbox", name="livedoor ID :").wait_for(timeout=config.WAIT_TIMEOUT)
        page.get_by_role("textbox", name="livedoor ID :").fill(config.LIVEDOOR_USER_ID)
        page.get_by_role("textbox", name="パスワード :").fill(config.LIVEDOOR_USER_PASSWD)
        page.get_by_role("button", name="Submit").click()

        # マイページが表示されるまで待つ
        page.get_by_role("link", name="マイページ").wait_for(timeout=config.WAIT_TIMEOUT)
        logging.info("✅ ログイン完了")
        return True

    except Exception as e:
        logging.error(f"❌ ログイン失敗: {e}")
        send_discord_log(f"❌ ログイン失敗: {e}")

        return False


def create_article(page, title, content):
    """記事を作成・投稿"""
    try:
        # 記事作成ページへ
        page.get_by_role("link", name="マイページ").click()
        page.get_by_role("link", name="記事を書く").click()
        page.locator("#entry_title").wait_for(timeout=config.WAIT_TIMEOUT)
        logging.info("📝 記事作成ページを開きました")

        # タイトル入力
        page.locator("#entry_title").fill(title)
        time.sleep(1)
        page.get_by_role("link", name="HTMLタグ編集").click()

        # 本文入力エリアにフォーカスして入力
        page.mouse.click(1124, 400)
        page.keyboard.insert_text(content)
        logging.info("📝 記事本文を入力しました")
        time.sleep(1)
        page.get_by_role("link", name="HTMLタグ編集").click()
        time.sleep(1)


        # 公開処理
        page.mouse.click(1105, 805)
        page.get_by_role("button", name="OK").click()
        logging.info("🚀 記事を投稿しました")
        return True
    except Exception as e:
        logging.error(f"❌ 記事投稿失敗: {e}")
        send_discord_log(f"❌ 記事投稿失敗: {e}")
        return False

def run_article_posting():
    """記事投稿のメイン処理"""
    playwright = None
    browser = None
    context = None
    
    try:
        logging.info(f"🕒 実行開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        send_discord_log(f"🕒 実行開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # with文を使わず、明示的に制御
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport=config.VIEWPORT)
        page = context.new_page()

        # AIから記事内容を取得
        res = gemini()
        title, content = thread2html(res)

        # ログインして記事投稿
        if login(page):
            if create_article(page, title, content):
                logging.info(f"✅ 投稿完了: {title}")
                send_discord_log(f"✅ 投稿完了: {title}")
                print(f"title: {title}\nで\n\n{content}\n\nで投稿しました")
            else:
                logging.error("❌ 記事投稿に失敗しました")
                send_discord_log("❌ 記事投稿に失敗しました")
        else:
            logging.error("❌ ログインに失敗しました")
            send_discord_log("❌ ログインに失敗しました")

    except Exception as e:
        logging.error(f"✖ 予期せぬエラー: {e}")
        send_discord_log(f"✖ 予期せぬエラー: {e}")

    finally:
        # 確実にリソースを解放
        try:
            if context:
                context.close()
            if browser:
                browser.close()
            if playwright:
                playwright.stop()  # 明示的に停止
        except Exception as e:
            logging.error(f"リソース解放中のエラー: {e}")
        
        logging.info(f"🏁 実行終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """メイン関数 - スケジューリング設定"""
    logging.info("🚀 スケジューラーを起動しました!!")
    send_discord_log("🚀 スケジューラーを起動しました!!")

    
    # スケジュール設定
    post_times = ["00:00", "07:00", "12:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

  
    for set_time in post_times:
        schedule.every().day.at(set_time).do(run_article_posting)

    
    # schedule.every(3).minutes.do(run_article_posting)

    
    logging.info(f"📅 スケジュール設定完了: {post_times}")

    # スケジューラー実行
    while True:
        try:
            schedule.run_pending()
            # time.sleep(10)
            time.sleep(300)
        except KeyboardInterrupt:
            logging.info("⏹️ スケジューラーを停止しました")
            send_discord_log("⏹️ スケジューラーを停止しました")
            break
        except Exception as e:
            logging.error(f"❌ スケジューラーエラー: {e}")
            send_discord_log(f"❌ スケジューラーエラー: {e}")

            time.sleep(60)


if __name__ == "__main__":
    # run_article_posting()
    # main()
    run_article_posting()

