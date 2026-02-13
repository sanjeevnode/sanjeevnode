import os
import requests
import re
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_quote():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [{
                "text": "Generate one short, powerful motivational quote for a software engineer. Maximum 20 words."
            }]
        }]
    }

    response = requests.post(url, json=payload)
    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"].strip()

def update_readme(quote):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_quote_block = f"""<!--QUOTE_START-->
> {quote}

_Last updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}_
<!--QUOTE_END-->"""

    updated_content = re.sub(
        r"<!--QUOTE_START-->.*?<!--QUOTE_END-->",
        new_quote_block,
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    quote = get_quote()
    update_readme(quote)
