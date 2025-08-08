import os
import requests
import cloudscraper
from bs4 import BeautifulSoup

# --- CONFIGURE THESE ---
# TELEGRAM_BOT_TOKEN = "8227969173:AAHCGgiAIN8uTyJpo8Tm3DniG5WF4JHSp9Q"
# TELEGRAM_CHAT_ID = "5692689924"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GRT_URL = "https://www.grtjewels.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_gold_rate():
    scraper = cloudscraper.create_scraper()
    response = scraper.get("https://www.grtjewels.com/")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    #headers = {
    #"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    #}
    #response = requests.get(GRT_URL, headers=headers)
    #soup = BeautifulSoup(response.content, "html.parser")
    print("soup.pretty", soup.prettify())

    # Finds the line containing "GOLD 22 KT/1g"
    rate_line = soup.find(text=lambda t: t and "GOLD 22 KT/1g" in t)
    print("rate_line", rate_line)
    
    rate_line_new = soup.find("span", string="22Kt Gold Rate")
    print("rate_line_new", rate_line_new)
    
    if not rate_line:
        return None

    # Expected format: 'GOLD 22 KT/1g - ₹ 9470'
    parts = rate_line.strip().split("₹")
    if len(parts) < 2:
        return None

    try:
        price = float(parts[1].strip().replace(",", ""))
        return price
    except ValueError:
        return None


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        r = requests.post(url, data=payload)
        if r.status_code != 200:
            print("Telegram message failed:", r.text)
    except Exception as e:
        print(f"Telegram error: {e}")


if __name__ == "__main__":
    rate = fetch_gold_rate()
    if rate:
        msg = f"✨ Today's 22K Gold Rate (GRT): ₹{rate:.2f}/g"
        print(msg)
        send_telegram_message(msg)
    else:
        err_msg = "❌ Failed to fetch 22K gold rate from GRT."
        print(err_msg)
        #send_telegram_message(err_msg)
