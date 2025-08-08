import requests
from bs4 import BeautifulSoup

URL = "https://www.grtjewels.com/"

def fetch_gold_rate():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Finds the line containing "GOLD 22 KT/1g"
    rate_line = soup.find(text=lambda t: t and "GOLD 22 KT/1g" in t)
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

if __name__ == "__main__":
    rate = fetch_gold_rate()
    if rate:
        print(f"✨ GRT Gold Rate (22K): ₹{rate} per gram")
    else:
        print("❌ Could not fetch the gold rate at this time.")
