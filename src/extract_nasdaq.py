# Nifra Wahaj | 25280002

import pandas as pd
from pathlib import Path
import logging
import kagglehub

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_nasdaq_data(tickers, start_date, end_date, output_dir):
    """
    Extract NASDAQ stock data from Kaggle dataset
    
    Args:
        tickers: List of stock tickers to extract
        start_date: Start date for data (YYYY-MM-DD)
        end_date: End date for data (YYYY-MM-DD)
        output_dir: Directory to save raw data
    
    Returns:
        DataFrame containing stock data
    """
    logger.info("Starting NASDAQ data extraction...")
    
    try:
        # Download dataset from Kaggle
        logger.info("Downloading NASDAQ dataset from Kaggle...")
        download_path = kagglehub.dataset_download("svaningelgem/nasdaq-daily-stock-prices")
        logger.info(f"Dataset downloaded to: {download_path}")
        
        dataset_path = Path(download_path)
        
        # Try to find individual ticker files
        all_dfs = []
        found_tickers = []
        
        for ticker in tickers:
            ticker_file = dataset_path / f"{ticker}.csv"
            if ticker_file.exists():
                logger.info(f"Reading {ticker} data from: {ticker_file}")
                df_ticker = pd.read_csv(ticker_file)
                
                # Add ticker column if it doesn't exist
                if 'ticker' not in df_ticker.columns:
                    df_ticker['ticker'] = ticker
                
                all_dfs.append(df_ticker)
                found_tickers.append(ticker)
            else:
                logger.warning(f"File not found for ticker: {ticker}")
        
        if not all_dfs:
            logger.error("No ticker files found. Trying to find combined file...")
            # Fallback: try to find the largest CSV
            csv_files = list(dataset_path.glob("*.csv"))
            if csv_files:
                csv_file = max(csv_files, key=lambda f: f.stat().st_size)
                logger.info(f"Reading combined file: {csv_file}")
                df_full = pd.read_csv(csv_file)
                
                # Find ticker column
                ticker_col = None
                for col in ['ticker', 'symbol', 'Symbol', 'Ticker']:
                    if col in df_full.columns:
                        ticker_col = col
                        break
                
                if ticker_col and ticker_col != 'ticker':
                    df_full.rename(columns={ticker_col: 'ticker'}, inplace=True)
                
                if ticker_col:
                    df = df_full[df_full['ticker'].isin(tickers)].copy()
                else:
                    df = df_full.copy()
            else:
                raise FileNotFoundError("No CSV files found in dataset")
        else:
            # Combine all ticker dataframes
            df = pd.concat(all_dfs, ignore_index=True)
            logger.info(f"Found data for tickers: {', '.join(found_tickers)}")
        
        logger.info(f"Total rows loaded: {len(df)}")
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Filter by date range
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        logger.info(f"Filtered to date range {start_date} to {end_date}: {len(df)} rows")
        
        # Sort by date and ticker
        df = df.sort_values(['ticker', 'date'])
        
        logger.info(f"Total stock records extracted: {len(df)}")
        
    except Exception as e:
        logger.error(f"Error extracting NASDAQ data: {e}", exc_info=True)
        df = pd.DataFrame()
    
    return df


def save_nasdaq_data(df, output_dir):
    """
    Save extracted NASDAQ data in multiple formats
    Args:
        df: DataFrame containing stock data
        output_dir: Directory to save data
    """
    if df.empty:
        logger.warning("No data to save")
        return
    
    output_path = Path(output_dir)
    
    # Save as CSV
    csv_path = output_path / "nasdaq_raw.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"NASDAQ data saved to CSV: {csv_path}")
    
    # Save as JSON
    json_path = output_path / "nasdaq_raw.json"
    df.to_json(json_path, orient="records", indent=2, date_format="iso")
    logger.info(f"NASDAQ data saved to JSON: {json_path}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"NASDAQ Stock Data Extraction Summary")
    logger.info(f"{'='*50}")
    logger.info(f"Total records: {len(df)}")
    logger.info(f"Tickers: {', '.join(df['ticker'].unique())}")
    logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
    logger.info(f"Columns: {', '.join(df.columns)}")
    logger.info(f"{'='*50}\n")