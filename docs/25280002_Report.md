# ELT Pipeline Report

Nifra Wahaj | 25280002


## Thematic Focus

This project analyzes the Financial Technology sector by integrating three complementary data sources: real time news coverage (NewsAPI), public search interest (Google Trends) and market performance (NASDAQ stock prices). The pipeline tracks how FinTech is discussed in media, searched online, and valued in financial markets from January 2023 through February 2026 (report based on data till 16 Februray 2026).


## Key Findings

- TechCrunch dominates FinTech coverage with 88% of articles, while Bloomberg and WSJ contribute minimally. FinTech is framed as tech innovation, not traditional finance.
- Broad FinTech terms ("fintech" ,"financial technology") generate 79% of coverage vs crypto specific topics (14%), indicating sector maturation beyond cryptocurrency origins
- Bitcoin search interest spikes to 100 in late 2024 and early 2026, but shows limited correlation with COIN stock prices—public search behavior and institutional trading operate on different timescales
- Strong correlations (0.90+) exist between COIN, META, and MSFT, indicating sector-wide movements
- COIN volatility is 3.2× higher (4.8%) than AAPL (1.5%)—crypto-related FinTech moves directionally with traditional tech but experiences amplified price swings
- NVDA shows negative correlations (-0.45 to -0.06) with most stocks, reflecting semiconductor cycles, not FinTech trends


## Technical Challenges Encountered

### Data Extraction
- NewsAPI rate limiting (100 requests/day) required careful keyword batching and sequential processing
- Content truncation limited text analysis as all articles clustered at 214 characters due to API truncation
- Google Trends rate limiting necessitated 2 second delays between requests to avoid IP blocks
- Kaggle dataset structure was undocumented, requiring fallback logic for missing ticker files (SQ ticker was not found)

### Data Quality
The Kaggle NASDAQ dataset proved exceptionally clean (zero missing values, zero duplicates, zero validation errors), preventing demonstration of handling messy data. While this simplified the cleaning pipeline, it meant the defensive validation code (checking for high < low, negative prices) executed but found no issues. This represents an approach where validation prevents future data quality degradation.

### Visualization
Static PNG visualizations limit interactivity as overlapping lines in temporal plots make individual stock tracking difficult. I concluded that to improve understandability, interactive Plotly dashboards with filtering and hover tooltips can be implemented in future.

## Pipeline Architecture

**Extract:** NewsAPI → Google Trends → Kaggle NASDAQ 
**Load:** Raw data → CSV + JSON formats → `data/raw/`  
**Transform:** Quality assessment → Validation → Feature engineering → `data/cleaned/`  
**Analyze:** Temporal, categorical and correlation visualizations → `visualizations/` 
