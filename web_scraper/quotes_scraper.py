import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://quotes.toscrape.com"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "quotes.json")


def scrape_quotes():
    url = BASE_URL
    all_data = []
    count = 1
    while url:
        if count==4:
            break
        print(f"Scraping: {url}")
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

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
    return all_data


def save_to_json(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved at:", DATA_PATH)


if __name__ == "__main__":
    print("Pagination scraping started...")
    data = scrape_quotes()
    save_to_json(data)
    print(f"Total quotes scraped: {len(data)}")