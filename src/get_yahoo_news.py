import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import time

# URL
url = "https://www.yahoo.co.jp/"

# URLにアクセスする 
req = requests.get(url)

# res.textをBeautifulSoupで扱うための処理
soup = BeautifulSoup(req.content, "html.parser")

# href属性に特定の文字が含まれているものを検索
elems = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))

# 取得した情報の数
num = len(elems)

# numpyライブラリで初期化
news = np.zeros((num,3), dtype='object')

# 保存するときにタイトル行は要れるので、データのみ格納
i = 0
for elem in elems:

    # ハイライト記事の取得
    res_detail = requests.get(elem.attrs['href'])
    soup_detail = BeautifulSoup(res_detail.content, "html.parser")
    elems_detail = soup_detail.find(class_=re.compile("highLightSearchTarget"))

    # データの格納

    news[i][0] = elem.text
    news[i][1] = elem.attrs['href']
    news[i][2] = elems_detail.text

    # サーバに負荷をかけないように待機（秒）
    time.sleep(1)

    i = i + 1

df = pd.DataFrame(news, columns=["title", "url", "highlight"])
df.to_csv("data_pandus.csv", index=False, encoding="utf-8-sig")
