#  Data Scraping Toolkit

> A full-stack project demonstrating email analysis, web scraping, and data extraction pipelines using Python, Node.js, MongoDB, and a simple frontend dashboard.

## Project Overview

This project is divided into two major parts:
1. **📧 Email Analyzer** (Inbox Data Processing)
2. **🌐 Web & Email Scraping Toolkit**

It showcases how data can be collected, processed, stored, and visualized in a structured way.

---

## 📁 Project Structure

```text
data-scraping-toolkit/
│
├── data/
│   └── quotes.json
│
├── Email_Analyzer/
│   ├── analyzer/
│   │   └── email_analyzer.py
│   ├── data/
│   │   └── inbox.mbox
│   ├── frontend/
│   │   └── index.html
│   ├── models/
│   │   └── email.model.js
│   ├── app.js
│   ├── index.js
│   ├── package.json
│   ├── .env
│   └── .gitignore
│
├── email_scraper/
│   └── email_extractor.py
│
├── web_scraper/
│   ├── backend/
│   ├── frontend/
│   └── quotes_scraper.py
│
└── README.md
```

## 📧 PART 1 — Email Analyzer

**Objective:** Parse exported `.mbox` email data to find specific keywords and display the results on a clean dashboard.

* **How it works:** A Node.js backend triggers a Python script to decode and read local inbox files. It filters the emails by your keyword, stores the structured data (Sender, Subject, Date, Body) in MongoDB, and serves it to the frontend UI.
* **Key Features:** * Fast keyword-based filtering.
  * Capable of processing large `.mbox` files (~180MB).
  * Automatically resolves unknown email encodings.
  * Seamless Backend ↔ Python communication.

---

## 🌐 PART 2 — Web & Email Scraping

**Objective:** Extract structured text (quotes) and email addresses from target websites using Python.

* **How it works:** Uses `requests` and `BeautifulSoup` to navigate web pages and handle pagination, saving scraped text to a JSON file. A secondary script utilizes Regex to hunt for and extract public email addresses from HTML.
* **Key Features:** * Automated pagination handling.
  * Precise regex-based pattern matching for emails.
  * Modular, lightweight, and easy to scale.
