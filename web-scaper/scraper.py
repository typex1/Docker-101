import requests
from bs4 import BeautifulSoup

def scrape_quotes():
    url = "https://quotes.toscrape.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = [quote.text for quote in soup.select(".quote .text")]
    for quote in quotes:
        print(quote)

if __name__ == "__main__":
    scrape_quotes()
