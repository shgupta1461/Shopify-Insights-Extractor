# Shopify Store Insights-Fetcher (Advanced)

This project is a professional, production-style FastAPI application that fetches insights from a Shopify storefront **without using the official Shopify API**. It features a fully asynchronous scraping pipeline, background task processing, a normalized database schema, and an improved UI.

## Advanced Features
- **Background Task Processing**: API endpoints respond instantly while scraping and data persistence occur in the background.
- **Dependency Injection**: Leverages FastAPI's `Depends` for clean, testable management of DB sessions and HTTP clients.
- **Normalized Database**: Stores insights in structured SQL tables (Product catalogue, Brands, Products, Policies, etc.) for robust querying, instead of a single JSON blob.
- **Resilient Scraping**: Includes a basic retry mechanism for network requests.
- **Competitor Analysis (Bonus)**: An endpoint to discover and scrape potential competitors.
- **Structured Logging**: Configured for clear, filterable application logs.
- **Polished UI**: A clean, modern frontend with improved user experience.

## Quick Start

**1. Setup Environment**
```bash
# Create and activate a virtual environment
python -m venv .venv
.venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
