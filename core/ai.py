import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(message):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Pihu, a friendly Indian female AI assistant. "
                    "Reply in Hindi and English mix. "
                    "Keep replies short and natural."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }

    response = requests.post(URL, headers=headers, json=data, timeout=30)

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]
if __name__ == "__main__":
    print(ask_ai("Hello"))