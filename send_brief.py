import os
import requests
import google.generativeai as genai
from datetime import datetime

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

def generate_brief():
    today = datetime.now().strftime("%A, %d %B %Y")
    prompt = f"""You are a financial and tech analyst. Write a concise daily briefing for {today} covering:

US Markets - Key index movements, what drove the market, one stock to watch.
Economics - Latest macro news (Fed, inflation, jobs, GDP) and what it means.
AI Trends - Biggest AI news, new model releases, business impact.

Format with emojis. Keep each section to 3-4 lines.
Start with: Daily Market Brief - {today}
"""
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt)
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
