# Nifra Wahaj | 25280002

import os
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"


for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, CLEANED_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# API Credentials 
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")


# NewsAPI configuration
NEWS_API_CONFIG = {
    "keywords": ["fintech", "cryptocurrency", "blockchain", "digital payments", "financial technology"],
    "domains": "techcrunch.com,reuters.com,bloomberg.com,wsj.com",
    "language": "en",
    "page_size": 100,
    "lookback_days": 30
}

# Google Trends configuration
PYTRENDS_CONFIG = {
    "keywords": ["bitcoin", "ethereum", "fintech", "blockchain", "cryptocurrency"],
    "timeframe": "2023-01-01 2026-02-14",
    "geo": "US"
}

# NASDAQ stock configuration
NASDAQ_CONFIG = {
    "tickers": ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "META", "COIN", "SQ", "PYPL"],
    "start_date": "2023-01-01",
    "end_date": "2026-02-14"
}

# Date range for analysis
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 2, 14)