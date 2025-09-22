from dotenv import load_dotenv
import os
from openai import OpenAI
from google import genai

load_dotenv()
PROMPT = os.getenv("PROMPT")
INSTRUCTIONS = os.getenv("INSTRUCTIONS")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def chatGPT() -> str:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=os.getenv(OPENAI_API_KEY))

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=INSTRUCTIONS,
        input=PROMPT,
    )

    print(response.output_text)
    with open("text.txt", mode="w", encoding="UTF-8") as f:
        f.write(response.output_text)

    return response.output_text


def gemini() -> str:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT
        )

    return response.text


def deepsheek() -> str:
    DEEPSHEEK_API_KEY = os.getenv("DEEPSHEEK_API_KEY")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=DEEPSHEEK_API_KEY)

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                # "content": "What is the meaning of life?"
                "content": PROMPT,
            }
        ],
    )
    print(completion.choices[0].message.content)
    with open("text.txt", mode="w", encoding="UTF-8") as f:
        f.write(completion.choices[0].message.content)

    return completion.choices[0].message.content


if __name__ == "__main__":
    # chatGPT()
    gemini()
    # deepsheek()
