import os
import requests
from bs4 import BeautifulSoup

URL = "https://eu.bungiestore.com/products/marathon-collector-s-edition-no-game-code/MAC24001-100"
TARGET_TEXT = "out of stock"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram_message(text: str):
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
        timeout=30,
    )
    response.raise_for_status()

def fetch_page(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text

def is_out_of_stock(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()
    return TARGET_TEXT.lower() in text

def main():
    send_telegram_message("workflow started")
    html = fetch_page(URL)
    if not is_out_of_stock(html):
        send_telegram_message(f"Похоже, товар появился в наличии: {URL}")
    else:
        send_telegram_message(f"Пока еще out of stock")
        ##print("Пока еще out of stock")

if __name__ == "__main__":
    main()
