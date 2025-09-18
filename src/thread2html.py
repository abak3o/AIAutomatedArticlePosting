import re
import json

def get_thread() -> str:
    with open("text.txt", mode="r", encoding="UTF-8") as f:
        data = f.read()
    return data

def format_thread2json(thread: str) -> str:
    split_list = re.split(r'(\n\^)', thread)
    thread_title = split_list[0].strip()
    thread_res = split_list[1:]
    thread_res_list = []
    post_number = 1
    
    for i in range(1, len(thread_res), 2):
        content = thread_res[i].strip()
        
        post_data = {
            "id": post_number,
            "user": "名無しのJ民",
            "userID": "dkdkdkd2",
            "content": content
        }
        
        thread_res_list.append(post_data)
        post_number += 1

    thread_data = {
        "title": thread_title,
        "thread_res": thread_res_list
    }
    
    json_output = json.dumps(thread_data, ensure_ascii=False, indent=2)
    
    return json_output

def convert_json2html(json_data):
    thread_data = json.loads(json_data)
    
    title = thread_data['title']
    posts = thread_data['thread_res']
    
    html_output = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
"""
    for post in posts:
        post_html = f"""
    <div>
        <p>{post['id']} ：{post['user']}</p>
        <p>{post['content']}</p>
    </div>
"""
        html_output += post_html
    html_output += """
</body>
</html>
"""
    
    return html_output


if __name__ == "__main__":
    text = get_thread()
    json_text = format_thread2json(text)
    print(json_text)

    html_result = convert_json2html(json_text)
    print(html_result)
    with open("index.html", mode="w", encoding="UTF-8") as f:
        f.write(html_result)        
