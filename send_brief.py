import os
import requests
from google import genai
from google.genai import types
from datetime import datetime

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
ALPHAVANTAGE_KEY = os.environ["ALPHAVANTAGE_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

def get_stock_prices():
    symbols = {"S&P 500": "SPY", "Nasdaq": "QQQ", "Dow Jones": "DIA"}
    results = {}
    for name, symbol in symbols.items():
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHAVANTAGE_KEY}"
        r = requests.get(url).json()
        quote = r.get("Global Quote", {})
        price = quote.get("05. price", "N/A")
        change = quote.get("10. change percent", "N/A")
        results[name] = f"{price} ({change})"
    return results

def get_crypto_prices():
    coins = ["bitcoin", "ethereum"]
    results = {}
    for coin in coins:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true"
        r = requests.get(url).json()
        price = r[coin]["usd"]
        change = round(r[coin]["usd_24h_change"], 2)
        results[coin.capitalize()] = f"${price:,} ({change}%)"
    return results

def get_fear_greed():
    url = "https://api.alternative.me/fng/?limit=1"
    r = requests.get(url).json()
    value = r["data"][0]["value"]
    label = r["data"][0]["value_classification"]
    return f"{value}/100 — {label}"

def get_news_headlines():
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    r = requests.get(url).json()
    headlines = [a["title"] for a in r.get("articles", [])[:5]]
    return "\n".join(f"- {h}" for h in headlines)

def get_yahoo_data():
    symbols = ["^GSPC", "^IXIC", "^DJI"]
    names = ["S&P 500", "Nasdaq", "Dow Jones"]
    results = {}
    for symbol, name in zip(symbols, names):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers).json()
        try:
            meta = r["chart"]["result"][0]["meta"]
            price = meta["regularMarketPrice"]
            prev = meta["chartPreviousClose"]
            change = round(((price - prev) / prev) * 100, 2)
            results[name] = f"{price:,.2f} ({'+' if change > 0 else ''}{change}%)"
        except:
            results[name] = "N/A"
    return results

def generate_brief():
    today = datetime.now().strftime("%A, %d %B %Y")

    stocks = get_stock_prices()
    yahoo = get_yahoo_data()
    crypto = get_crypto_prices()
    fear_greed = get_fear_greed()
    news = get_news_headlines()

    data_summary = f"""
LIVE MARKET DATA FOR {today}:

📈 US Markets (Yahoo Finance):
- S&P 500: {yahoo.get('S&P 500')}
- Nasdaq: {yahoo.get('Nasdaq')}
- Dow Jones: {yahoo.get('Dow Jones')}

📈 US Markets (Alpha Vantage ETFs):
- S&P 500 (SPY): {stocks.get('S&P 500')}
- Nasdaq (QQQ): {stocks.get('Nasdaq')}
- Dow Jones (DIA): {stocks.get('Dow Jones')}

🪙 Crypto:
- Bitcoin: {crypto.get('Bitcoin')}
- Ethereum: {crypto.get('Ethereum')}

😨 Fear & Greed Index: {fear_greed}

📰 Top Business Headlines:
{news}
"""

    prompt = f"""You are a financial and tech analyst. Today is {today}.

Here is LIVE real data collected right now:
{data_summary}

Using this real data above AND searching the web for more context, write a daily briefing:

📈 US Markets
- Use the real numbers above
- Explain what drove the market today
- One stock to watch

🪙 Crypto
- Use the real BTC and ETH prices above
- Brief market sentiment

😨 Market Sentiment
- Reference the Fear & Greed Index above
- What it signals for investors

🏦 Economics
- Latest Fed, inflation, jobs, GDP news
- What it means

🤖 AI Trends
- Biggest AI news today
- New releases or research

Write it TWICE:
First in English starting with: 📅 Daily Market Brief — {today}
Then separator: ——————————————
Then same content in Thai starting with: 📅 สรุปตลาดประจำวัน — {today}

Keep each section to 3-4 lines. Be specific with real numbers.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
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
