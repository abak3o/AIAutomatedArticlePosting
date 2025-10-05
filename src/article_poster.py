import time
import logging
from config import config
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright
from ai import chatGPT, gemini, deepseek
from thread2html import thread2html
from discord import send_discord_log

# ログ設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class ArticlePoster:

    def __init__(self, userID, userPasswd):
        self.logger = logging.getLogger(__name__)
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.id = userID
        self.passwd = userPasswd


    def setup(self):
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(viewport=config.VIEWPORT)
            self.page = self.context.new_page()
            self.logger.info("ブラウザを起動しました")
            self.logger.info("🌐 ブラウザを起動しました")
            return True
        except Exception as e:
            self.logger.error(f"❌ ブラウザ起動失敗: {e}")
            return False


    def teardown(self):
        """リソースの解放 - このメソッドを追加"""
        try:
            if self.page:
                self.page.close()
                self.logger.info("📄 ページを閉じました")
            if self.context:
                self.context.close()
                self.logger.info("🔒 コンテキストを閉じました")
            if self.browser:
                self.browser.close()
                self.logger.info("🌐 ブラウザを閉じました")
            if self.playwright:
                self.playwright.stop()
                self.logger.info("🛑 Playwrightを停止しました")
        except Exception as e:
            self.logger.warning(f"リソース解放中の警告: {e}")


    def login(self):
        """ログイン処理"""
        try:
            self.page.goto(config.LIVEDOOR_URL)
            self.page.get_by_role("textbox", name="livedoor ID :").wait_for(
                timeout=config.WAIT_TIMEOUT
            )
            self.page.get_by_role("textbox", name="livedoor ID :").fill(self.id)
            self.page.get_by_role("textbox", name="パスワード :").fill(self.passwd)
            self.page.get_by_role("button", name="Submit").click()

            # マイページが表示されるまで待つ
            self.page.get_by_role("link", name="マイページ").wait_for(
                timeout=config.WAIT_TIMEOUT
            )
            self.logger.info("✅ ログイン完了")
            return True

        except Exception as e:
            self.logger.error(f"❌ ログイン失敗: {e}")
            send_discord_log(f"❌ ログイン失敗: {e}")
            return False


def generate_article(self) -> tuple[str, str]:
    max_retries = 2
    forbidden_keywords = ["AI", "ラーメン", "焼肉", "スーパー", "コンビニ"]  # 実際のキーワードに置き換え
    
    for attempt in range(max_retries):
        try:
            res = gemini()
            title, content = thread2html(res)
            
            # タイトルクリーニング
            title = title.replace("記事タイトル", "").strip()
            
            # 禁止キーワードチェック
            if any(keyword in title for keyword in forbidden_keywords):
                self.logger.warning(f"試行 {attempt + 1}: 禁止キーワード検出 - {title}")
                continue  # 再生成
                
            if not title or not content:
                self.logger.warning(f"試行 {attempt + 1}: 空のタイトルまたは本文")
                continue  # 再生成
            
            self.logger.info(f"📄 記事生成完了: {title}")
            return title, content
            
        except Exception as e:
            self.logger.warning(f"試行 {attempt + 1} 失敗: {e}")
            if attempt == max_retries - 1:  # 最終試行
                self.logger.error("❌ 記事生成失敗")
                send_discord_log(f"❌ 記事生成失敗: {e}")
                raise
    
    raise ValueError(f"{max_retries}回試行しましたが記事を生成できませんでした")


    def create_article(self, title: str, content: str) -> bool:
        """記事を作成・投稿"""
        try:
            # 記事作成ページへ
            self.page.get_by_role("link", name="マイページ").click()
            self.page.get_by_role("link", name="記事を書く").click()
            self.page.locator("#entry_title").wait_for(timeout=config.WAIT_TIMEOUT)
            self.logger.info("📝 記事作成ページを開きました")

            # タイトル入力
            self.page.locator("#entry_title").fill(title)
            time.sleep(1)
            self.page.get_by_role("link", name="HTMLタグ編集").click()

            # 本文入力
            self.page.mouse.click(1124, 400)
            self.page.keyboard.insert_text(content)
            self.logger.info("📝 記事本文を入力しました")
            time.sleep(1)
            self.page.get_by_role("link", name="HTMLタグ編集").click()
            time.sleep(1)

            # 公開処理
            self.page.mouse.click(1105, 805)
            self.page.get_by_role("button", name="OK").click()
            self.logger.info("🚀 記事を投稿しました")
            return True

        except Exception as e:
            self.logger.error(f"❌ 記事投稿失敗: {e}")
            send_discord_log(f"❌ 記事投稿失敗: {e}")
            return False


    def run(self) -> dict:
        """記事投稿のメイン処理 - 1回だけ実行"""
        start_time = datetime.now()

        # セットアップ
        if not self.setup():
            return {"status": "error", "message": "ブラウザの起動に失敗しました"}

        try:
            self.logger.info(f"🕒 実行開始: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            send_discord_log(f"🕒 実行開始: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

            # 記事生成
            title, content = self.generate_article()

            # ログインして記事投稿
            if self.login():
                if self.create_article(title, content):
                    result = {
                        "status": "success",
                        "title": title,
                        "message": "記事投稿が完了しました",
                        "execution_time": str(datetime.now() - start_time),
                    }
                    self.logger.info(f"✅ 投稿完了: {title}")
                    send_discord_log(f"✅ 投稿完了: {title}")
                    print(f"title: {title}\nで投稿しました")
                    return result
                else:
                    raise Exception("記事投稿に失敗しました")
            else:
                raise Exception("ログインに失敗しました")

        except Exception as e:
            self.logger.error(f"✖ 予期せぬエラー: {e}")
            send_discord_log(f"✖ 予期せぬエラー: {e}")
            return {
                "status": "error",
                "message": str(e),
                "execution_time": str(datetime.now() - start_time),
            }

        finally:
            # 確実にリソース解放
            self.teardown()
            end_time = datetime.now()
            self.logger.info(f"🏁 実行終了: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    poster = ArticlePoster(config.LIVEDOOR_USER_ID, config.LIVEDOOR_USER_PASSWD)
    poster.run()
