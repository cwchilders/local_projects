# Zillow Scraper Project

This project is a Python-based web scraper designed to extract key metrics (views, saves, and days on market) and property facts from Zillow listings. The data is scraped using Playwright for robust bot detection avoidance and stored in a lightweight SQLite database for historical tracking and analysis.

## 📁 Project Structure

The project is organized into modular Python files, separating the core functionalities for better maintainability and readability.

* `main_scraper.py`: The main script that orchestrates the scraping process. It handles command-line arguments, reads URLs, and calls functions from the other modules.

* `scrape_zillow.py`: Contains the core scraping logic using Playwright to handle navigation, wait for elements, and retrieve the page's HTML content.

* `parse_zillow_page.py`: Responsible for parsing the HTML content of a Zillow page to extract both property stats (views, saves, etc.) and property facts (beds, baths, etc.).

* `zillow_db.py`: A wrapper module for all SQLite database interactions. It handles connecting to the database, setting up tables, and inserting new scrape results.

* `zillow_property_manager.py`: Contains utility functions for parsing property information, such as extracting the unique Zillow Property ID (ZPID) and the property name from a URL.

* `zillow_listing_urls.txt`: A text file where you should place the URLs of the Zillow listings you want to scrape, with one URL per line.

## 🚀 Getting Started

### Prerequisites

* Python 3.x

* `requests` library (`pip install requests`)

* `beautifulsoup4` library (`pip install beautifulsoup4`)

* `playwright` library (`pip install playwright`)

* `playwright-stealth` library (`pip install playwright-stealth`)

### Setup and Installation

1. **Clone or download the project files.**

2. **Create a Python virtual environment** (recommended):

```

python -m venv venv
source venv/bin/activate  \# On Windows, use `venv\Scripts\activate`

```

3. **Install the required libraries**:

```

pip install -r requirements.txt

```

(Note: A `requirements.txt` file is not included by default. You can create one with `pip freeze > requirements.txt` after installing the above packages.)

4. **Install the necessary browsers for Playwright**:

```

playwright install

```

5. **Create your URL list**:
Open the `zillow_listing_urls.txt` file and add the Zillow URLs you want to scrape, one per line. For example:

```

[https://www.zillow.com/homedetails/309-Floresta-St-Las-Vegas-NM-87701/242094031\_zpid/](https://www.zillow.com/homedetails/309-Floresta-St-Las-Vegas-NM-87701/242094031_zpid/)
[https://www.zillow.com/homedetails/123-Anytown-Rd-Somewhere-FL/12345678\_zpid/](https://www.google.com/search?q=https://www.zillow.com/homedetails/123-Anytown-Rd-Somewhere-FL/12345678_zpid/)

```

### Running the Scraper

Run the `main_scraper.py` script from your terminal.

```

python main\_scraper.py

```

The script will:

* Automatically create or connect to an SQLite database file named `zillow_data.db`.

* Read the URLs from `zillow_listing_urls.txt`.

* Scrape the data for each URL using Playwright.

* Save the scrape results to the database.

## 🗃️ Database

The project uses a local SQLite database file named `zillow_data.db`. The database schema is designed to store property information, time-series scrape data, and agent details.

### Viewing the Database

You can view and query the database using the command-line tool or a VS Code extension.

**From the terminal**:

```

sqlite3 zillow\_data.db ".schema"

```

This will print the table creation scripts to the console.

**With a VS Code Extension**:
The **SQLite Viewer** extension by Florian Klampfe is highly recommended. To use it, simply right-click the `zillow_data.db` file in the Explorer and select `Open with SQLite Viewer`.

## 🤝 Contributing

Feel free to improve this project by adding new features, fixing bugs, or refactoring the code
```
