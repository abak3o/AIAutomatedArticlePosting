import os
import datetime
import logging
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright

# ログ設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# 環境変数読み込み
load_dotenv()
LIVEDOOR_URL = os.getenv("LIVEDOOR_URL")
LIVEDOOR_USER_ID = os.getenv("LIVEDOOR_USER_ID")
LIVEDOOR_USER_PASSWD = os.getenv("LIVEDOOR_USER_PASSWD")

# 定数
VIEWPORT = {"width": 1920, "height": 1000}
WAIT_TIMEOUT = 10000  # 10秒


def login(page):
    """ログイン処理"""
    page.goto(LIVEDOOR_URL)
    page.get_by_role("textbox", name="livedoor ID :").fill(LIVEDOOR_USER_ID)
    page.get_by_role("textbox", name="パスワード :").fill(LIVEDOOR_USER_PASSWD)
    page.get_by_role("button", name="Submit").click()

    # マイページが表示されるまで待つ
    page.get_by_role("link", name="マイページ").wait_for(timeout=WAIT_TIMEOUT)
    logging.info("✅ ログイン完了")


def create_article(page, title, content):
    """記事を作成・投稿"""
    # 記事作成ページへ
    page.get_by_role("link", name="マイページ").click()
    page.get_by_role("link", name="記事を書く").click()
    page.locator("#entry_title").wait_for(timeout=WAIT_TIMEOUT)
    logging.info("📝 記事作成ページを開きました")

    # タイトル入力
    page.locator("#entry_title").fill(title)

    # 本文入力エリアにフォーカスして入力
    page.mouse.click(1124, 400)
    page.keyboard.insert_text(content)
    logging.info("📝 記事本文を入力しました")

    # 公開処理
    page.mouse.click(1105, 805)
    page.get_by_role("button", name="OK").click()
    logging.info("🚀 記事を投稿しました")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport=VIEWPORT)
    page = context.new_page()

    # 記事内容
    dt_now = datetime.datetime.now()
    content = f"投稿内容 {dt_now}"
    title = "article_title"

    # 処理実行
    login(page)
    create_article(page, title, content)

    # クローズ処理
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
