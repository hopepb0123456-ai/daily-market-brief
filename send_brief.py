import os
import requests
from google import genai
from datetime import datetime

TELEGRAM_TOKEN = os.environ[8729073556:AAH2m_XF76WZM2RA04bfd-EMf1OkLbXZVSo]
CHAT_ID = os.environ[-1003651166776]
GEMINI_API_KEY = os.environ[AIzaSyBzyU422gM71CykUbEYhNpYCBs-UObM-58]

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_brief():
    today = datetime.now().strftime("%A, %d %B %Y")
    prompt = f"""You are a financial and tech analyst. Write a concise daily briefing for {today} covering:

📈 US Markets
- Key index movements (S&P 500, Nasdaq, Dow Jones)
- What drove the market today
- One stock to watch

🏦 Economics
- Latest macro news (Fed, inflation, jobs, GDP)
- What it means for investors

🤖 AI Trends
- Biggest AI news today
- New model releases or research
- Business impact

Format with emojis. Keep each section to 3-4 lines.
Start with: 📅 Daily Market Brief — {today}
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    print(response.json())

if __name__ == "__main__":
    brief = generate_brief()
    send_telegram(brief)
    print("✅ Brief sent!")
