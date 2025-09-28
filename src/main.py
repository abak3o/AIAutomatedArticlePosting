from article_poster import ArticlePoster
from config import config

def main():
    poster = ArticlePoster(config.LIVEDOOR_USER_ID, config.LIVEDOOR_USER_PASSWD)
    poster.run()


if __name__ == "__main__":
    main()

"""
TODO: 
- local fastAPI
    - /XXX-run みたいな形でアカウン毎にプログラムを走らせる
    - /ALL-run も欲しい 環境変数をしっかり
- local docker
- gcp cloud run
- cloud scheduler
"""