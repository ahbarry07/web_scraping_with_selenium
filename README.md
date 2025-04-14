# web_scraping_with_selenium

## Euronews Just-In Article Scraper

This project is a Python-based web scraper that collects the latest news articles from the [Euronews Just-In page](https://www.euronews.com/just-in) using Selenium with a headless Chrome browser.

## 📌 Features

- Loads multiple articles dynamically (up to 750).
- Extracts article title, URL, date, and time.
- Retrieves the full body content of each article.
- Saves results to a CSV file: `data/scraped_news.csv`.
- Logs progress and errors to `scraping.log`.

## 🛠️ Requirements

- Python 3.8+
- Google Chrome
- Chromedriver (automatically managed via `webdriver-manager`)

## 📦 Installation

```bash
git clone https://github.com/your-username/euronews-scraper.git
cd euronews-scraper
pip install -r requirements.txt
```

Create a `requirements.txt` with:

```
selenium
webdriver-manager
pandas
```

## 🚀 Usage

Simply run the script:

```bash
python scraper.py
```

This will:
- Launch a headless Chrome session
- Load additional articles (50 times)
- Extract basic metadata (title, date, link)
- Visit each article to extract the body content
- Save the data to a CSV file
- Save logs to `scraping.log`

## 🧐 Code Overview

### `setup_driver()`
Initializes a headless Chrome browser using Selenium and WebDriver Manager.

### `load_more_articles(driver)`
Simulates clicking the "Load More" button 50 times to fetch more articles.

### `extract_articles(article)`
Parses the article element for title, link, and date.

### `get_article_content(driver, article)`
Navigates to the full article page and scrapes the body content.

### `scraper_news()`
The main asynchronous function that coordinates everything.

## 📝 Output

- CSV file: `data/scraped_news.csv`
- Log file: `scraping.log`

## 🛡️ Notes

- The script ignores videos and watch articles.
- Articles without body content are skipped.
- Duplicate links are removed before saving the file.

## 📁 Folder Structure

```
.
├── data/
│   └── scraped_news.csv
├── logs/
│   └── scraping.log
├── scraper.py
└── README.md
```

## 🪠 Troubleshooting

- Make sure Chrome is installed on your system.
- If articles are not loading, inspect the page structure—it may have changed.
- If `scraping.log` is not created, check your file permissions or logging configuration.

## 📃 License

This project is open-source and available under the MIT License.

