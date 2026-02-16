# Nifra Wahaj | 25280002

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_news_data(api_key, keywords, domains, language, page_size, lookback_days, output_dir):
    """
    Args:
        api_key: NewsAPI authentication key
        keywords: List of keywords to search for
        domains: Comma-separated list of news domains
        language: Language code (e.g., 'en')
        page_size: Number of articles per request
        lookback_days: How many days back to fetch news
        output_dir: Directory to save raw data
    """
    logger.info("Starting NewsAPI extraction...")
    
    if not api_key:
        raise ValueError("NEWS_API_KEY not found in environment variables")
    
    # Calculate date range
    to_date = datetime.now()
    from_date = to_date - timedelta(days=lookback_days)
    
    base_url = "https://newsapi.org/v2/everything"
    all_articles = []
    
    for keyword in keywords:
        logger.info(f"Fetching articles for keyword: {keyword}")
        
        params = {
            "q": keyword,
            "apiKey": api_key,
            "language": language,
            "domains": domains,
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "pageSize": page_size,
            "sortBy": "publishedAt"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                logger.info(f"Retrieved {len(articles)} articles for '{keyword}'")
                
                # Add keyword to each article
                for article in articles:
                    article["search_keyword"] = keyword
                    all_articles.append(article)
            else:
                logger.warning(f"API returned status: {data.get('status')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for '{keyword}': {e}")
    
    df = pd.DataFrame(all_articles)
    
    if not df.empty:
        raw_json_path = Path(output_dir) / "newsapi_raw.json"
        with open(raw_json_path, "w") as f:
            json.dump(all_articles, f, indent=2)
        logger.info(f"Raw JSON saved to {raw_json_path}")
        
        # Remove duplicates based on URL
        df = df.drop_duplicates(subset=["url"], keep="first")
        logger.info(f"Total unique articles extracted: {len(df)}")
    else:
        logger.warning("No articles extracted from NewsAPI")
    
    return df


def save_news_data(df, output_dir):
    if df.empty:
        logger.warning("No data to save")
        return
    
    output_path = Path(output_dir)
    
    csv_path = output_path / "newsapi_raw.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"News data saved to CSV: {csv_path}")
    
    json_path = output_path / "newsapi_structured.json"
    df.to_json(json_path, orient="records", indent=2, date_format="iso")
    logger.info(f"News data saved to JSON: {json_path}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"NewsAPI Extraction Summary")
    logger.info(f"{'='*50}")
    logger.info(f"Total articles: {len(df)}")
    logger.info(f"Date range: {df['publishedAt'].min()} to {df['publishedAt'].max()}")
    logger.info(f"Unique sources: {df['source'].apply(lambda x: x.get('name') if isinstance(x, dict) else x).nunique()}")
    logger.info(f"{'='*50}\n")