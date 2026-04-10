import requests
import re
import sys
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["scraper_db"]
collection = db["emails"]

def extract_emails(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Failed to fetch page")
            return []

        emails = re.findall(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
            response.text
        )

        return list(set(emails))

    except Exception as e:
        print(e)
        return []


if __name__ == "__main__":
    url = sys.argv[1]

    emails = extract_emails(url)

    if emails:
        collection.delete_many({})
        collection.insert_many([{"email": e} for e in emails])
        print("Emails saved")
    else:
        print("No emails found")