# Customer Experience Analytics for Ethiopian Fintech Apps

Analyze Google Play Store reviews for three Ethiopian banks to uncover customer satisfaction drivers and pain points.

## Target Banks
- **CBE** - Commercial Bank of Ethiopia
- **BOA** - Bank of Abyssinia  
- **Dashen** - Dashen Bank

## Project Structure
```
├── data/
│   ├── raw/                 # Raw scraped reviews
│   └── processed/           # Cleaned and analyzed data
├── notebooks/
│   ├── task1_data_collection.ipynb    # Scraping & preprocessing
│   └── task2_sentiment_analysis.ipynb # Sentiment & themes
├── src/
│   ├── config.py            # Configuration settings
│   ├── scraper.py           # Google Play scraper
│   ├── preprocessing.py     # Data cleaning pipeline
│   ├── sentiment_analyzer.py # VADER & DistilBERT sentiment
│   └── theme_analyzer.py    # TF-IDF thematic analysis
└── tests/
```

## Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

## Task 1: Data Collection & Preprocessing

### Methodology
1. **Scraping**: Use `google-play-scraper` with `reviews_all()` to collect all available reviews
2. **Preprocessing Pipeline**:
   - Remove duplicates
   - Handle missing values
   - Normalize dates to YYYY-MM-DD
   - Clean text (whitespace, special characters)
   - Filter English-only reviews
   - Validate ratings (1-5)

### Output
- `data/processed/reviews_processed.csv` with columns: `review_id`, `review_text`, `rating`, `review_date`, `bank_name`, `source`

## Task 2: Sentiment & Thematic Analysis

### Sentiment Analysis

**Two methods implemented for comparison:**

| Method | Type | Description |
|--------|------|-------------|
| VADER | Rule-based | Fast, uses sentiment lexicon, good for social media text |
| DistilBERT | Transformer | Deep learning, understands context, more accurate |

**Output**: `sentiment_label` (POSITIVE/NEGATIVE/NEUTRAL), `sentiment_score` (0-1 confidence)

### Thematic Analysis

**Methodology:**
1. **Preprocessing**: Lowercase, remove special chars, lemmatize with spaCy
2. **Keyword Extraction**: TF-IDF with n-grams (1-3 words)
3. **Theme Mapping**: Match keywords to predefined business themes

### Theme Categories & Grouping Logic

| Theme | Keywords | Rationale |
|-------|----------|-----------|
| **Account Access Issues** | login, password, authentication, otp, verification, locked | User authentication and account access problems |
| **Transaction Performance** | transfer, slow, fast, speed, transaction, payment, send, receive | Money movement and transaction speed |
| **User Interface & Experience** | ui, interface, design, easy, difficult, confusing, user-friendly | App usability and visual design |
| **Technical Issues** | crash, bug, error, freeze, not working, fail, glitch | App stability and technical problems |
| **Customer Support** | support, help, service, response, contact, complaint | Customer service quality |
| **Feature Requests** | feature, add, need, want, should, update, improve | User suggestions for improvements |
| **Security & Privacy** | security, safe, secure, fingerprint, biometric, privacy | Security features and concerns |

### Output
- `data/processed/reviews_with_sentiment_themes.csv` with added columns:
  - `sentiment_label_vader`, `sentiment_score_vader`
  - `sentiment_label_distilbert`, `sentiment_score_distilbert`
  - `themes`, `primary_theme`, `matched_keywords`

## Running the Analysis

```bash
# Run Task 1 notebook
jupyter notebook notebooks/task1_data_collection.ipynb

# Run Task 2 notebook
jupyter notebook notebooks/task2_sentiment_analysis.ipynb
```

## Requirements
See `requirements.txt` for full list. Key dependencies:
- `google-play-scraper` - Review scraping
- `transformers` + `torch` - DistilBERT sentiment
- `vaderSentiment` - VADER sentiment
- `scikit-learn` - TF-IDF
- `spacy` - NLP preprocessing
