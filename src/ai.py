from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

def chatGPT() -> str:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PROMPT = os.getenv("PROMPT")
    INSTRUCTIONS = os.getenv("INSTRUCTIONS")
    client = OpenAI(api_key=os.getenv(OPENAI_API_KEY))


    response = client.responses.create(
        model="gpt-5-mini",
        # instructions="You are a coding assistant that talks like a pirate.",
        instructions=INSTRUCTIONS,
        input=PROMPT,
    )
    print(response.output_text)
    with open("text.txt", mode="w", encoding="UTF-8") as f:
        f.write(response.output_text)
    return response.output_text

if __name__ == "__main__":
    chatGPT()
    