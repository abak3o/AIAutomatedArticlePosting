from openai import OpenAI
from google import genai
from config import config
import google.generativeai as genai
from google.generativeai.types import GenerationConfig



def chatGPT() -> str:
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-5-mini",
        instructions=config.INSTRUCTIONS,
        input=config.PROMPT,
    )
    return response.output_text


def gemini() -> str:
    # APIキーを設定
    genai.configure(api_key=config.GOOGLE_API_KEY)

    # モデルを初期化
    model = genai.GenerativeModel(config.GEMINI_MODEL)

    # temperature を含む生成設定
    generation_config = GenerationConfig(
        temperature=0.85
    )

    # コンテンツを生成
    response = model.generate_content(
        contents=config.PROMPT,
        generation_config=generation_config
    )

    return response.text

def deepseek() -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1", api_key=config.DEEPSEEK_API_KEY
    )
    resuponse = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                # "content": "What is the meaning of life?"
                "content": config.PROMPT,
            }
        ],
    )
    return resuponse.choices[0].message.content


def get_ai_response():
    pass


if __name__ == "__main__":
    # res = chatGPT()
    res = gemini()
    # res = deepseek()
    print(res)
