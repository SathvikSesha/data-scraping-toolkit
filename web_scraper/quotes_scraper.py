import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://quotes.toscrape.com"

def scrape_quotes():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")

    data = []

    for i in range(min(len(quotes),5)):
        data.append({
            "quote": quotes[i].text,
            "author": authors[i].text,
            "length": len(quotes[i].text)
        })

    return data


import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "quotes.json")

def save_to_json(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved at:", DATA_PATH)

if __name__ == "__main__":
    print("Scraping started...")
    data = scrape_quotes()
    save_to_json(data)
    print("Data saved successfully!")