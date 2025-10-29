import requests
from bs4 import BeautifulSoup
import time

def scrape_quotes():
    url = "https://quotes.toscrape.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = [quote.text for quote in soup.select(".quote .text")]
    for quote in quotes:
        print(quote)

if __name__ == "__main__":
    while True:
        print(f"Scraping at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        scrape_quotes()
        print("Waiting 60 seconds before next scrape...")
        time.sleep(60)  # Wait 60 seconds between scrapes
