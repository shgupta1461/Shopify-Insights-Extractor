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
```

## DEMO

<img width="950" height="463" alt="image" src="https://github.com/user-attachments/assets/50289531-d46c-4bac-85e4-be41b68c78a0" />
<img width="954" height="475" alt="image" src="https://github.com/user-attachments/assets/7843f66f-c61a-4056-ba33-f5efea8b243e" />
<img width="953" height="473" alt="image" src="https://github.com/user-attachments/assets/1567018c-c447-4cd5-9f18-6c49746b506e" />
<img width="956" height="475" alt="image" src="https://github.com/user-attachments/assets/e212a868-72d9-4172-8ee6-ae9c26c6182a" />
<img width="954" height="475" alt="image" src="https://github.com/user-attachments/assets/4c7565b7-2748-4ea9-8605-db0c5117953a" />
<img width="953" height="476" alt="image" src="https://github.com/user-attachments/assets/2cd4ae1c-660e-4870-9ba8-97c887bc4874" />


<img width="953" height="376" alt="image" src="https://github.com/user-attachments/assets/8cee0d29-66ba-4fa8-98cf-2e68fe03cab8" />
<img width="952" height="475" alt="image" src="https://github.com/user-attachments/assets/8c0e4fa6-0ced-4ce7-86a4-34cb44987ae3" />
<img width="955" height="477" alt="image" src="https://github.com/user-attachments/assets/c17ea600-eab4-4ca5-b79c-3ca04ce5eae9" />

#### Backend
<img width="533" height="218" alt="image" src="https://github.com/user-attachments/assets/6fb45cd7-1731-45b8-a6df-95390439b4a8" />











# Run the app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
