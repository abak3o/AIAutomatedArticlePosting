from openai import OpenAI
from google import genai
from config import config


def chatGPT() -> str:
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-5-mini",
        instructions=config.INSTRUCTIONS,
        input=config.PROMPT,
    )

    return response.output_text


def gemini() -> str:
    client = genai.Client(api_key=config.GOOGLE_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=config.PROMPT
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


if __name__ == "__main__":
    # res = chatGPT()
    # res = gemini()
    res = deepseek()
    print(res)
