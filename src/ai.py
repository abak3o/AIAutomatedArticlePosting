from dotenv import load_dotenv
import os
from openai import OpenAI
from google import genai

load_dotenv()
PROMPT = os.getenv("PROMPT")
INSTRUCTIONS = os.getenv("INSTRUCTIONS")

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

    response = client.models.generate_content(model="gemini-2.5-flash", contents=PROMPT)
    print(response.text)
    with open("text.txt", mode="w", encoding="UTF-8") as f:
        f.write(response.text)

    return response.text


if __name__ == "__main__":
    # chatGPT()
    gemini()
