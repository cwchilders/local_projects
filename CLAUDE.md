# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-project repository containing two main components:

1. **Real Estate/Zillow Scraper** (`/real_estate/`) - A Python-based web scraper for extracting property data from Zillow listings
2. **Climate Data Analysis** (`/climate/`) - Meteorological data analysis using the Meteostat library
3. **YouTube API Project** (`/youtube_api/`) - Basic YouTube API integration (minimal implementation)

## Common Commands

### Python Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (required for Zillow scraper)
playwright install
```

### Real Estate Scraper
```bash
# Main scraper execution
python real_estate/scrape_zillow.py

# Process scraped data
python real_estate/process_zillow_scrapes.py

# Parse individual pages
python real_estate/parse_zillow_page.py

# Run tests
python real_estate/test_parse_zillow.py
```

### Climate Data Analysis
```bash
# Generate Santa Fe temperature analysis
python climate/meteostat/test_santa_fe.py
```

## Architecture

### Real Estate Scraper Architecture

The Zillow scraper follows a modular design with clear separation of concerns:

- **`scrape_zillow.py`** - Core scraping logic using Playwright with stealth mode for bot detection avoidance
- **`parse_zillow_page.py`** - HTML parsing and data extraction using BeautifulSoup
- **`zillow_db.py`** - SQLite database operations and schema management
- **`zillow_property_manager.py`** - Property URL parsing and ZPID extraction utilities
- **`zillow_file_manager.py`** - File operations and data persistence
- **`zillow_image_manager.py`** - Image extraction and management
- **`process_zillow_scrapes.py`** - Batch processing orchestrator

### Data Flow
1. URLs are read from `zillow_listing_urls.txt`
2. Playwright scrapes HTML content with stealth mode
3. BeautifulSoup parses property stats and facts
4. Data is stored in SQLite database (`zillow_data.db`)
5. Images and formatted output are saved to respective directories

### Configuration
- **`real_estate_config.py`** - Centralized configuration for directories and settings
- **`config/API_KEYS.json`** - API keys storage (not tracked in git)
- **`config/real_estate.json`** - Real estate specific configurations

### Key Dependencies
- `playwright` + `playwright-stealth` for web scraping
- `beautifulsoup4` for HTML parsing
- `sqlite3` for data storage
- `meteostat` for climate data analysis
- `google-api-python-client` for YouTube API integration

## Data Storage

The project uses SQLite for persistence with the following schema:
- `properties` table - Property metadata and URLs
- `scrape_results` table - Time-series scraping results
- `listing_agents` table - Agent information

Database file: `real_estate/zillow_data.db`

## Output Structure

- `real_estate/output/` - Formatted property data in Markdown and HTML
- `real_estate/page_scrapes/` - Raw scraped content
- `real_estate/test/` - Property image galleries organized by address
- `SantaFe.png` - Climate analysis output chart