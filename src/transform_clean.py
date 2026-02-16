# Nifra Wahaj | 25280002

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataQualityReport:    
    def __init__(self, df, dataset_name):
        self.df = df
        self.dataset_name = dataset_name
        self.report = {}
    
    def assess_quality(self):
        logger.info(f"\n{'='*60}")
        logger.info(f"Quality Assessment: {self.dataset_name}")
        logger.info(f"{'='*60}")
        
        # Basic statistics
        self.report['total_records'] = len(self.df)
        self.report['total_columns'] = len(self.df.columns)
        
        # Missing values
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        self.report['missing_values'] = {
            col: {
                'count': int(missing[col]),
                'percentage': float(missing_pct[col])
            }
            for col in self.df.columns if missing[col] > 0
        }
        
        # Duplicate records
        duplicates = self.df.duplicated().sum()
        self.report['duplicate_records'] = int(duplicates)
        self.report['duplicate_percentage'] = float((duplicates / len(self.df)) * 100)
        
        # Data types
        self.report['data_types'] = {col: str(dtype) for col, dtype in self.df.dtypes.items()}
        
        #  summary
        logger.info(f"Total Records: {self.report['total_records']:,}")
        logger.info(f"Total Columns: {self.report['total_columns']}")
        logger.info(f"\nMissing Values:")
        if self.report['missing_values']:
            for col, stats in self.report['missing_values'].items():
                logger.info(f"  - {col}: {stats['count']} ({stats['percentage']:.2f}%)")
        else:
            logger.info("  No missing values found")
        
        logger.info(f"\nDuplicate Records: {self.report['duplicate_records']} ({self.report['duplicate_percentage']:.2f}%)")
        logger.info(f"{'='*60}\n")
        
        return self.report


def clean_newsapi_data(raw_dir, processed_dir, cleaned_dir):
    """
    Clean and transform NewsAPI data
    
    Args:
        raw_dir: Directory containing raw data
        processed_dir: Directory for processed data
        cleaned_dir: Directory for cleaned data
        """
    logger.info("Cleaning NewsAPI data...")
    
    df = pd.read_csv(Path(raw_dir) / "newsapi_raw.csv")
    qa = DataQualityReport(df, "NewsAPI")
    quality_report = qa.assess_quality()
    logger.info("Applying cleaning transformations...")
    
    # Handle missing values
    # Drop rows where title or description is missing (critical fields)
    initial_count = len(df)
    df = df.dropna(subset=['title', 'description'])
    logger.info(f"Removed {initial_count - len(df)} rows with missing title/description")
    
    # Fill missing content with description
    df['content'] = df['content'].fillna(df['description'])
    
    # Fill missing author with 'Unknown'
    df['author'] = df['author'].fillna('Unknown')
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['url'], keep='first')
    logger.info(f"Removed {initial_count - len(df)} duplicate records")
    
    #Standardize dates
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    df = df.dropna(subset=['publishedAt'])
    
    #  Extract source name from source dict
    df['source_name'] = df['source'].apply(
        lambda x: eval(x)['name'] if isinstance(x, str) else (x.get('name') if isinstance(x, dict) else 'Unknown')
    )
    
    # Add derived features
    df['text_length'] = df['content'].str.len()
    df['title_length'] = df['title'].str.len()
    df['has_image'] = df['urlToImage'].notna()
    
    # Select and order columns
    df = df[['publishedAt', 'source_name', 'author', 'title', 'description', 
             'content', 'url', 'urlToImage', 'search_keyword', 'text_length', 
             'title_length', 'has_image']]
    

    output_path = Path(cleaned_dir) / "newsapi_cleaned.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Cleaned data saved: {output_path}")
    
    report_path = Path(processed_dir) / "newsapi_quality_report.json"
    with open(report_path, 'w') as f:
        json.dump(quality_report, f, indent=2)
    logger.info(f"Quality report saved: {report_path}\n")
    
    return df


def clean_nasdaq_data(raw_dir, processed_dir, cleaned_dir):
    logger.info("Cleaning NASDAQ data...")
    
    df = pd.read_csv(Path(raw_dir) / "nasdaq_raw.csv")
    qa = DataQualityReport(df, "NASDAQ Stocks")
    quality_report = qa.assess_quality()
    
    logger.info("Applying cleaning transformations...")
    
    #  Handle missing values
    initial_count = len(df)
    # drop rows with missing OHLC values
    df = df.dropna(subset=['open', 'high', 'low', 'close'])
    logger.info(f"Removed {initial_count - len(df)} rows with missing price data")
    
    #  Remove duplicates
    df = df.drop_duplicates(subset=['ticker', 'date'], keep='first')
    
    #  Standardize dates
    df['date'] = pd.to_datetime(df['date'])
    
    # Data validation
    # Remove records where high < low (data quality issue)
    invalid_mask = df['high'] < df['low']
    if invalid_mask.sum() > 0:
        logger.warning(f"Found {invalid_mask.sum()} records with high < low. Removing...")
        df = df[~invalid_mask]
    
    # Remove records with negative prices
    price_cols = ['open', 'high', 'low', 'close']
    for col in price_cols:
        negative_mask = df[col] < 0
        if negative_mask.sum() > 0:
            logger.warning(f"Found {negative_mask.sum()} records with negative {col}. Removing...")
            df = df[~negative_mask]
    
    # Add derived features
    # Daily return
    df = df.sort_values(['ticker', 'date'])
    df['daily_return'] = df.groupby('ticker')['close'].pct_change()
    
    # Price range
    df['price_range'] = df['high'] - df['low']
    df['price_range_pct'] = (df['price_range'] / df['open']) * 100
    
    # Moving averages (7 day and 30 day)
    df['ma_7'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    df['ma_30'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=30, min_periods=1).mean())
    
    # Volatility (7 day rolling standard deviation of returns)
    df['volatility_7d'] = df.groupby('ticker')['daily_return'].transform(lambda x: x.rolling(window=7, min_periods=1).std())
    
    # Sort by ticker and date
    df = df.sort_values(['ticker', 'date'])
    
    output_path = Path(cleaned_dir) / "nasdaq_cleaned.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Cleaned data saved: {output_path}")
    
    report_path = Path(processed_dir) / "nasdaq_quality_report.json"
    with open(report_path, 'w') as f:
        json.dump(quality_report, f, indent=2)
    logger.info(f"Quality report saved: {report_path}\n")
    
    return df


def generate_summary_statistics(df, dataset_name):

    logger.info(f"\nSummary Statistics: {dataset_name}")
    logger.info("="*60)
    
    # Get numerical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        summary = df[numeric_cols].describe()
        logger.info(f"\n{summary}")
    else:
        logger.info("No numerical columns found")
    
    logger.info("="*60 + "\n")


def run_cleaning_pipeline(raw_dir, processed_dir, cleaned_dir):
    """
    Run the complete cleaning and transformation pipeline
    """
    logger.info("="*60)
    logger.info("STARTING DATA CLEANING PIPELINE")
    logger.info("="*60 + "\n")
    
    # Clean NewsAPI data
    news_df = clean_newsapi_data(raw_dir, processed_dir, cleaned_dir)
    generate_summary_statistics(news_df, "NewsAPI")
    
    # Clean NASDAQ data
    nasdaq_df = clean_nasdaq_data(raw_dir, processed_dir, cleaned_dir)
    generate_summary_statistics(nasdaq_df, "NASDAQ Stocks")
    
    logger.info("="*60)
    logger.info("DATA CLEANING PIPELINE COMPLETED")
    logger.info("="*60 + "\n")
    
    return news_df, nasdaq_df


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))    
    import config
    run_cleaning_pipeline(config.RAW_DATA_DIR, config.PROCESSED_DATA_DIR, config.CLEANED_DATA_DIR)