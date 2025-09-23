import re
import json
import random
from ai import chatGPT, gemini, deepseek


def get_thread() -> str:
    with open("text.txt", mode="r", encoding="UTF-8") as f:
        data = f.read()
    return data


def format_thread2json(thread: str) -> str:
    # split_list = re.split(r'(\n\^)', thread)
    split_list = re.split(r"(\n\^)", thread)

    thread_title = split_list[0].strip()
    thread_res = split_list[1:]
    thread_res_list = []
    post_number = 1

    thread_count = 0
    for i in range(1, len(thread_res), 2):
        if thread_count >= 90:
            break

        content = thread_res[i].strip()

        post_data = {"id": post_number, "user": "名無しのJ民", "content": content}

        thread_res_list.append(post_data)
        random_num = random.randint(1, 4)
        post_number += random_num
        thread_count += 1

    thread_data = {"title": thread_title, "thread_res": thread_res_list}

    json_output = json.dumps(thread_data, ensure_ascii=False, indent=2)

    print(json_output)
    return json_output

def convert_json2html(json_data):
    thread_data = json.loads(json_data)

    title = thread_data["title"]
    posts = thread_data["thread_res"]

    # CSSスタイル定義
    css_style = """
<style type='text/css'>
.id-line {
  font-size: 81.25%;
}
.user-name {
  color: rgb(0, 128, 0);
}
.post-content {
  font-weight: bold;
  white-space: pre-line;
}
.thread-title {
  color: #333;
}
.post-container {
  margin-bottom: 20px;
  padding: 10px;
  border-left: 3px solid #eee;
}
</style>
"""

    html_output = f"<div class='thread-title'><h1>{title}</h1></div>\n"

    for post in posts:
        # コンテンツ内の改行を処理
        content = post['content'].replace('\n', '<br>')
        
        post_html = f"""
<div class='post-container'>
    <p class='id-line'>{post['id']}：<span class='user-name'>{post['user']}</span></p>
    <p class='post-content'>{content}</p>
</div>
"""
        html_output += post_html

    # CSSをHTMLの先頭に追加
    html_output = css_style + html_output

    with open("index.html", mode="w", encoding="UTF-8") as f:
        f.write(html_output)

    return title, html_output


def thread2html(thread):
    json_text = format_thread2json(thread)
    title, html = convert_json2html(json_text)

    return title, html


if __name__ == "__main__":
    # text = get_thread()
    text = gemini()
    title, html = thread2html(text)
