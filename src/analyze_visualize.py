# Nifra Wahaj | 25280002

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def create_temporal_analysis(cleaned_dir, output_dir):
    """
    Visualization 1: Stock price trends over time
    """
    logger.info("Creating temporal analysis visualizations...")
    
    # Load cleaned NASDAQ data
    nasdaq_df = pd.read_csv(Path(cleaned_dir) / "nasdaq_cleaned.csv")
    nasdaq_df['date'] = pd.to_datetime(nasdaq_df['date'])
    
    # Load Google Trends data
    trends_df = pd.read_csv(Path(cleaned_dir).parent / "raw" / "pytrends_raw.csv")
    trends_df['date'] = pd.to_datetime(trends_df['date'])
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Stock closing prices over time
    ax1 = axes[0]
    for ticker in nasdaq_df['ticker'].unique():
        ticker_data = nasdaq_df[nasdaq_df['ticker'] == ticker]
        ax1.plot(ticker_data['date'], ticker_data['close'], label=ticker, linewidth=2, alpha=0.8)
    
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Closing Price ($)', fontsize=12)
    ax1.set_title('NASDAQ Stock Closing Prices - Financial Technology Sector', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper left', ncol=3)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Google Trends interest over time
    ax2 = axes[1]
    # Get keyword columns 
    keyword_cols = [col for col in trends_df.columns if col != 'date']
    for keyword in keyword_cols:
        ax2.plot(trends_df['date'], trends_df[keyword], label=keyword, linewidth=2, alpha=0.8)
    
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Search Interest', fontsize=12)
    ax2.set_title('Google Trends: FinTech Keyword Search Interest Over Time', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper left', ncol=3)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = Path(output_dir) / "temporal_analysis.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logger.info(f"Temporal analysis saved: {output_path}")
    plt.close()


def create_categorical_analysis(cleaned_dir, output_dir):
    """
    Visualization 2: News article distribution
    """
    logger.info("Creating categorical analysis visualizations...")
    
    news_df = pd.read_csv(Path(cleaned_dir) / "newsapi_cleaned.csv")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Articles by source
    ax1 = axes[0]
    source_counts = news_df['source_name'].value_counts().head(10)
    source_counts.plot(kind='barh', ax=ax1, color='steelblue')
    ax1.set_xlabel('Number of Articles', fontsize=12)
    ax1.set_ylabel('News Source', fontsize=12)
    ax1.set_title('Top 10 News Sources - FinTech Coverage', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Plot 2: Articles by keyword
    ax2 = axes[1]
    keyword_counts = news_df['search_keyword'].value_counts()
    keyword_counts.plot(kind='bar', ax=ax2, color='coral')
    ax2.set_xlabel('Search Keyword', fontsize=12)
    ax2.set_ylabel('Number of Articles', fontsize=12)
    ax2.set_title('Article Distribution by Search Keyword', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = Path(output_dir) / "categorical_analysis.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logger.info(f"Categorical analysis saved: {output_path}")
    plt.close()


def create_correlation_analysis(cleaned_dir, output_dir):
    """
    Visualization 3: Stock price correlations and volatility analysis
    """
    logger.info("Creating correlation analysis visualizations...")
    
    # Load cleaned NASDAQ data
    nasdaq_df = pd.read_csv(Path(cleaned_dir) / "nasdaq_cleaned.csv")
    nasdaq_df['date'] = pd.to_datetime(nasdaq_df['date'])
    
    price_pivot = nasdaq_df.pivot(index='date', columns='ticker', values='close')
    correlation_matrix = price_pivot.corr()
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    
    # Plot 1: Correlation heatmap
    ax1 = axes[0]
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, ax=ax1, cbar_kws={'label': 'Correlation'})
    ax1.set_title('Stock Price Correlation Matrix - FinTech Sector', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Stock Ticker', fontsize=11)
    ax1.set_ylabel('Stock Ticker', fontsize=11)
    
    # Plot 2: Volatility comparison
    ax2 = axes[1]
    volatility_data = nasdaq_df.groupby('ticker')['volatility_7d'].mean().sort_values(ascending=False)
    volatility_data.plot(kind='bar', ax=ax2, color='indianred')
    ax2.set_xlabel('Stock Ticker', fontsize=11)
    ax2.set_ylabel('Average 7-Day Volatility', fontsize=11)
    ax2.set_title('Average Stock Volatility - FinTech Companies', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = Path(output_dir) / "correlation_analysis.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logger.info(f"Correlation analysis saved: {output_path}")
    plt.close()


def run_analysis_pipeline(cleaned_dir, output_dir):

    logger.info("="*60)
    logger.info("STARTING ANALYSIS AND VISUALIZATION PIPELINE")
    logger.info("="*60 + "\n")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    create_temporal_analysis(cleaned_dir, output_dir)
    create_categorical_analysis(cleaned_dir, output_dir)
    create_correlation_analysis(cleaned_dir, output_dir)
    
    logger.info("\n" + "="*60)
    logger.info("ANALYSIS AND VISUALIZATION PIPELINE COMPLETED")
    logger.info(f"Visualizations saved to: {output_dir}")
    logger.info("="*60 + "\n")


if __name__ == "__main__":
    import sys
    from pathlib import Path    
    sys.path.append(str(Path(__file__).parent.parent))
    import config
    
    PROJECT_ROOT = Path(__file__).parent.parent
    run_analysis_pipeline(config.CLEANED_DATA_DIR, PROJECT_ROOT / "visualizations")