# Nifra Wahaj | 25280002

from pytrends.request import TrendReq
import pandas as pd
from pathlib import Path
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_trends_data(keywords, timeframe, geo, output_dir):
    """
    Extract Google Trends data for specified keywords
    Args:
        keywords: List of keywords to track
        timeframe: Time range for trends (e.g., '2023-01-01 2026-02-14')
        geo: Geographic location code (e.g., 'US')
        output_dir: Directory to save raw data
    """
    logger.info("Starting Google Trends extraction...")
    
    pytrends = TrendReq(hl='en-US', tz=360)
    all_trends = []
    
    # Process keywords in batches of 5 to avoid rate limits
    batch_size = 5
    for i in range(0, len(keywords), batch_size):
        batch = keywords[i:i+batch_size]
        logger.info(f"Fetching trends for: {', '.join(batch)}")
        
        try:
            # Build payload
            pytrends.build_payload(batch, cat=0, timeframe=timeframe, geo=geo, gprop='')
            
            # Get interest over time
            interest_df = pytrends.interest_over_time()
            
            if not interest_df.empty:
                # Remove 'isPartial' column if it exists
                if 'isPartial' in interest_df.columns:
                    interest_df = interest_df.drop('isPartial', axis=1)
                
                all_trends.append(interest_df)
                logger.info(f"Retrieved {len(interest_df)} time periods for batch")
            
            # Sleep to avoid rate limiting
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error fetching trends for batch {batch}: {e}")
    
    # Combine all trends data
    if all_trends:
        df = pd.concat(all_trends, axis=1)
        # Remove duplicate columns if any
        df = df.loc[:, ~df.columns.duplicated()]
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'date'}, inplace=True)
        logger.info(f"Total trends data points: {len(df)}")
    else:
        logger.warning("No trends data extracted")
        df = pd.DataFrame()
    
    return df


def save_trends_data(df, output_dir):
    """
    Save extracted trends data in multiple formats
    
    Args:
        df: DataFrame containing trends data
        output_dir: Directory to save data
    """
    if df.empty:
        logger.warning("No data to save")
        return
    
    output_path = Path(output_dir)
    
    csv_path = output_path / "pytrends_raw.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"Trends data saved to CSV: {csv_path}")
    
    json_path = output_path / "pytrends_raw.json"
    df.to_json(json_path, orient="records", indent=2, date_format="iso")
    logger.info(f"Trends data saved to JSON: {json_path}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Google Trends Extraction Summary")
    logger.info(f"{'='*50}")
    logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
    logger.info(f"Keywords tracked: {', '.join([col for col in df.columns if col != 'date'])}")
    logger.info(f"Total time periods: {len(df)}")
    logger.info(f"{'='*50}\n")