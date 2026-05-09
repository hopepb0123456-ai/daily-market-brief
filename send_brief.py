import os
import requests
from google import genai
from datetime import datetime

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_brief():
    today = datetime.now().strftime("%A, %d %B %Y")
    prompt = f"""You are a financial and tech analyst. Write a daily briefing for {today}.

Write it in TWO sections:

FIRST write in English:
📅 Daily Market Brief — {today}

📈 US Markets
- Key index movements (S&P 500, Nasdaq, Dow Jones)
- What drove the market
- One stock to watch

🏦 Economics
- Latest macro news (Fed, inflation, jobs, GDP)
- What it means for investors

🤖 AI Trends
- Biggest AI news today
- New model releases or research
- Business impact

Then write a separator line: ——————————————

THEN write the SAME content translated in Thai:
📅 สรุปตลาดประจำวัน — {today}

Use the same 3 sections but in Thai.
Keep each section to 3-4 lines. Format with emojis. Be specific and insightful.
"""
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return response.text

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    print(response.json())

if __name__ == "__main__":
    brief = generate_brief()
    send_telegram(brief)
    print("Brief sent!")
