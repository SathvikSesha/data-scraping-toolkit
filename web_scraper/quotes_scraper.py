import requests
from bs4 import BeautifulSoup
import json
import os
import time
from pymongo import MongoClient

BASE_URL = "https://quotes.toscrape.com"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "quotes.json")

client = MongoClient("mongodb://localhost:27017/")
db = client["scraper_db"]
collection = db["quotes"]

def scrape_quotes():
    url = BASE_URL
    all_data = []
    count = 1
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        }
    while url:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        print(response.status_code)
        quotes = soup.find_all("span", class_="text")
        authors = soup.find_all("small", class_="author")

        for i in range(len(quotes)):
            all_data.append({
                "quote": quotes[i].text,
                "author": authors[i].text,
                "length": len(quotes[i].text),
                "page": count
            })

        next_btn = soup.find("li", class_="next")
        if next_btn:
            next_link = next_btn.find("a")["href"]
            url = BASE_URL + next_link
        else:
            url = None
        count+=1
        time.sleep(1)
    return all_data


# def save_to_json(data):
#     os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

#     with open(DATA_PATH, "w") as f:
#         json.dump(data, f, indent=4)

#     print("Saved at:", DATA_PATH)

def save_to_mongoDB(data):
    collection.insert_many(data)
    print("Data saved to MongoDB!")

if __name__ == "__main__":
    print("Pagination scraping started...")
    data = scrape_quotes()
    save_to_mongoDB(data)
    print(f"Total quotes scraped: {len(data)}")