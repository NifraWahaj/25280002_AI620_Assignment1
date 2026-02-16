# Financial Technology ELT Pipeline

**Author:** Nifra Wahaj  
**Student ID:** 25280002  
**Thematic Domain:** Financial Technology

---

## Project Overview

This project implements a complete Extract-Load-Transform (ELT) pipeline integrating multiple real-world data sources related to Financial Technology. The pipeline extracts data from APIs, public datasets, and time-series sources, stores it in CSV + JSON, performs quality assessment and cleaning and generates visualizations.

### Data Sources

1. **NewsAPI** - FinTech news articles (API source, semi-structured JSON)
2. **Google Trends** - Search interest for FinTech keywords (time-series, structured)
3. **Kaggle NASDAQ** - Historical stock prices (public dataset, structured)

### Key Results

- **57 news articles** from TechCrunch, Bloomberg, WSJ (Jan-Feb 2026)
- **163 time periods** of search trends (2023-2026)
- **6,016 stock records** across 8 FinTech/tech companies

**View Pipeline:** [`docs/pipeline_diagram.jpg`](docs/pipeline_diagram.jpg)  
**Assignment Analytical Answers:** [`docs/answers.md`](docs/answers.md)  
**Brief Summary Report:** [`docs/report.md`](docs/report.md)

---

## Project Structure
```
PA1/
├── config.py                  # Pipeline configuration
├── run_all.py                 # Complete pipeline orchestrator
├── requirements.txt           # Python dependencies
│
├── src/                       # Extraction & transformation modules
│   ├── extract_newsapi.py
│   ├── extract_pytrends.py
│   ├── extract_nasdaq.py
│   ├── transform_clean.py
│   └── analyze_visualize.py
│
├── data/
│   ├── raw/                   # Extracted data (CSV + JSON)
│   ├── cleaned/               # Transformed datasets
│   └── processed/             # Quality reports (JSON)
│
├── visualizations/            # Generated charts 
│   ├── temporal_analysis.png
│   ├── categorical_analysis.png
│   └── correlation_analysis.png
│
└── docs/
    ├── answers.md             # Assignment responses
    ├── report.md              # Executive summary
    └── pipeline_diagram.jpg   # Architecture diagram
```

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- pip
- Kaggle account
- NewsAPI account

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure NewsAPI

1. Sign up at [newsapi.org](https://newsapi.org/)
2. Get your API key
3. Create `.env` file in project root:
```bash
NEWS_API_KEY=your_api_key_here
```

### 3. Configure Kaggle

1. Create account at [kaggle.com](https://www.kaggle.com/)
2. Go to Settings → API → Create New Token
3. Download `kaggle.json` and place it:
```bash
# Mac/Linux
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Windows
mkdir %USERPROFILE%\.kaggle
move %USERPROFILE%\Downloads\kaggle.json %USERPROFILE%\.kaggle\
```

---

## Running the Pipeline

```bash
python run_all.py
```

**Steps executed:**
1. Extract data from NewsAPI, Google Trends, NASDAQ
2. Clean and transform data with quality checks
3. Generate 3 visualizations

---

## Output Files

| Directory | Contents |
|-----------|----------|
| `data/raw/` | Raw extracted data in CSV + JSON formats |
| `data/cleaned/` | Cleaned datasets with derived features (moving averages, volatility, returns) |
| `data/processed/` | Quality assessment reports (missing values, duplicates, metrics) |
| `visualizations/` | 3 PNG charts (temporal trends, categorical distributions, correlations) |

---

## Configuration

Edit `config.py` to customize:
```python
# Stock tickers
NASDAQ_CONFIG = {
    "tickers": ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "META", "COIN", "PYPL"]
}

# News keywords
NEWS_API_CONFIG = {
    "keywords": ["fintech", "cryptocurrency", "blockchain", "digital payments"]
}

# Trends keywords
PYTRENDS_CONFIG = {
    "keywords": ["bitcoin", "ethereum", "fintech", "blockchain", "cryptocurrency"]
}
```

---

## Key Findings

- TechCrunch dominates with 88% of FinTech articles; broad "fintech" terms generate 79% coverage vs crypto-specific topics (14%)
- Bitcoin search trendds spikes to 100 but shows limited correlation with COIN stock prices
- COIN exhibits 4.8% volatility, 3.2× higher than AAPL (1.5%) and crypto moves with tech directionally but with amplified swings
- NVDA shows negative correlations (-0.45 to -0.06) with most stocks, reflecting semiconductor cycles

---

## Data Attribution

- **NewsAPI:** [newsapi.org](https://newsapi.org/)
- **Google Trends:** [trends.google.com](https://trends.google.com/)
- **NASDAQ Dataset:** [Kaggle - NASDAQ Daily Stock Prices](https://www.kaggle.com/datasets/svaningelgem/nasdaq-daily-stock-prices)
