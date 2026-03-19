import os
import requests
import time
import random
from playwright.sync_api import sync_playwright
from datetime import datetime

URL = "https://eu.bungiestore.com/products/marathon-collector-s-edition-no-game-code/MAC24001-100"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram_message(text: str) -> None:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
        timeout=30,
    )
    response.raise_for_status()


def fetch_rendered_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)

        html = page.content()
        browser.close()
        return html


def is_out_of_stock(html: str) -> bool:
    html = html.lower()
    return (
        "this product is currently not available for purchase." in html
        or "this product is out of stock. you cannot add it to your bag." in html
    )


def main() -> None:
    html = fetch_rendered_html(URL)

    if not is_out_of_stock(html):
        send_telegram_message(f"Похоже, товар появился в наличии: {URL}")
    else:
        send_telegram_message(f"out of stock")


if __name__ == "__main__":
    main()
    sleep_seconds = random.randint(300, 600)
    time.sleep(sleep_seconds)
