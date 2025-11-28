# 🏦 Ethiopian Bank Reviews Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ethiopianbankreview.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Overview

**Ethiopian Bank Reviews Analytics** is a comprehensive customer experience analysis platform that extracts, processes, and visualizes Google Play Store reviews for Ethiopia's leading mobile banking applications. The project leverages Natural Language Processing (NLP) techniques including sentiment analysis and thematic clustering to uncover actionable insights about customer satisfaction drivers and pain points.

This solution helps banking executives, product managers, and UX researchers understand customer feedback at scale, enabling data-driven decisions to improve mobile banking experiences for millions of Ethiopian users.

**🔗 Live Dashboard**: [ethiopianbankreview.streamlit.app](https://ethiopianbankreview.streamlit.app/)

---

## ✨ Features

- **Automated Data Collection**: Scrape thousands of reviews from Google Play Store using `google-play-scraper`
- **Multi-Method Sentiment Analysis**: Compare VADER (rule-based) and DistilBERT (transformer-based) sentiment classification
- **Thematic Analysis**: TF-IDF keyword extraction with business-relevant theme categorization
- **PostgreSQL Integration**: Structured data storage with normalized schema for scalable analytics
- **Interactive Dashboard**: Real-time filtering, KPI cards, and interactive Plotly visualizations
- **Bank Comparison**: Side-by-side performance metrics across Commercial Bank of Ethiopia, Bank of Abyssinia, and Dashen Bank
- **Trend Analysis**: Monthly satisfaction rate tracking and pain point identification
- **Cloud Deployment**: Production-ready Streamlit Cloud deployment

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.10+ |
| **Data Processing** | Pandas, NumPy |
| **NLP & ML** | Transformers (DistilBERT), VADER, spaCy, scikit-learn |
| **Database** | PostgreSQL, SQLAlchemy |
| **Visualization** | Plotly, Matplotlib, Seaborn, WordCloud |
| **Dashboard** | Streamlit |
| **Scraping** | google-play-scraper |
| **Environment** | python-dotenv |

---

## 📁 Project Structure

```
Ethiopian-Bank-Reviews/
│
├── 📂 dashboard/
│   ├── app.py                    # Streamlit dashboard application
│   ├── requirements.txt          # Dashboard-specific dependencies
│   └── data/
│       └── reviews_final.csv     # Exported data for cloud deployment
│
├── 📂 notebooks/
│   ├── task1_data_collection.ipynb      # Data scraping & preprocessing
│   ├── task2_sentiment_analysis.ipynb   # Sentiment & thematic analysis
│   └── task4_insights_recommendations.ipynb  # Insights & visualizations
│
├── 📂 src/
│   ├── __init__.py
│   ├── config.py                 # Configuration & environment variables
│   ├── scraper.py                # Google Play Store scraper
│   ├── preprocessing.py          # Data cleaning pipeline
│   ├── sentiment_analyzer.py     # VADER & DistilBERT sentiment
│   ├── theme_analyzer.py         # TF-IDF thematic analysis
│   └── database.py               # PostgreSQL connection & operations
│
├── 📂 data/
│   ├── raw/                      # Raw scraped reviews
│   └── processed/                # Cleaned and analyzed data
│
├── 📂 scripts/
│   └── run_pipeline.py           # End-to-end pipeline runner
│
├── 📂 .streamlit/
│   └── config.toml               # Streamlit theme configuration
│
├── .env.example                  # Environment variables template
├── .gitignore
├── requirements.txt              # Project dependencies
├── schema.sql                    # PostgreSQL database schema
├── LICENSE
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 14+ (optional, for database storage)
- Git

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/Filimon-H/Google-Play-Store-Reviews.git
cd Google-Play-Store-Reviews

# 2. Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy language model
python -m spacy download en_core_web_sm

# 5. Set up environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials (if using database)
```

---

## 💻 Usage

### Running the Dashboard (Recommended)

```bash
# Local dashboard with CSV data (no database required)
streamlit run dashboard/app.py
```

Access at: `http://localhost:8501`

### Running Jupyter Notebooks

```bash
# Start Jupyter
jupyter notebook

# Then open notebooks in order:
# 1. notebooks/task1_data_collection.ipynb
# 2. notebooks/task2_sentiment_analysis.ipynb
# 3. notebooks/task4_insights_recommendations.ipynb
```

### Running the Full Pipeline

```bash
# Execute complete data pipeline
python scripts/run_pipeline.py
```

### Database Operations (Optional)

```bash
# Test database connection
python test_database.py

# Export data to CSV for dashboard
python export_data_for_dashboard.py
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bank_reviews
DB_USER=your_username
DB_PASSWORD=your_password

# Scraping Configuration (optional)
REVIEWS_PER_BANK=1500
MAX_RETRIES=3
```

### Target Banks Configuration (`src/config.py`)

```python
APP_IDS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp',
}

BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'Dashen': 'Dashen Bank',
}
```

---

## 📊 Data Description

### Dataset Overview

| Attribute | Description |
|-----------|-------------|
| **Source** | Google Play Store |
| **Banks** | CBE, Bank of Abyssinia, Dashen Bank |
| **Total Reviews** | 7,290+ |
| **Date Range** | 2014 - 2024 |
| **Language** | English (filtered) |

### Data Schema

| Column | Type | Description |
|--------|------|-------------|
| `review_id` | STRING | Unique review identifier |
| `review_text` | TEXT | User review content |
| `rating` | INT | Star rating (1-5) |
| `review_date` | DATE | Review submission date |
| `bank_name` | STRING | Full bank name |
| `sentiment_label_vader` | STRING | VADER sentiment (POSITIVE/NEGATIVE) |
| `sentiment_score_vader` | FLOAT | VADER confidence score |
| `sentiment_label_distilbert` | STRING | DistilBERT sentiment |
| `sentiment_score_distilbert` | FLOAT | DistilBERT confidence score |
| `primary_theme` | STRING | Main identified theme |
| `themes` | JSON | All matched themes |

### Preprocessing Steps

1. **Duplicate Removal**: Eliminate identical reviews
2. **Missing Value Handling**: Drop reviews without text
3. **Date Normalization**: Convert to `YYYY-MM-DD` format
4. **Text Cleaning**: Remove special characters, normalize whitespace
5. **Language Filtering**: Keep English reviews only (using `langdetect`)
6. **Rating Validation**: Ensure ratings are 1-5

---

## 🔬 Methodology

### 1. Data Collection
- Scrape reviews using `google-play-scraper` library
- Collect metadata: rating, date, review text, app version
- Target: 400+ reviews per bank after preprocessing

### 2. Preprocessing Pipeline
- 8-step cleaning process in `preprocessing.py`
- Language detection to filter non-English reviews
- Text normalization for consistent analysis

### 3. Sentiment Analysis

| Method | Approach | Strengths |
|--------|----------|-----------|
| **VADER** | Rule-based lexicon | Fast, interpretable, good for social media |
| **DistilBERT** | Transformer neural network | Context-aware, higher accuracy |

### 4. Thematic Analysis

```
TF-IDF Vectorization → Keyword Extraction → Theme Mapping
```

**Theme Categories:**
- Account Access Issues
- Transaction Performance
- User Interface & Experience
- Technical Issues
- Customer Support
- Feature Requests
- Security & Privacy

### 5. Visualization & Insights
- Interactive Plotly charts
- Trend analysis over time
- Bank comparison metrics
- Pain point identification

---

## 📈 Results

### Key Findings

| Bank | Avg Rating | Positive % | Top Pain Point |
|------|------------|------------|----------------|
| Dashen Bank | 4.12 ⭐ | 68% | Feature Requests |
| Commercial Bank of Ethiopia | 3.82 ⭐ | 58% | Technical Issues |
| Bank of Abyssinia | 2.86 ⭐ | 42% | Transaction Performance |

### Sentiment Distribution

![Sentiment Distribution](images/sentiment_distribution.png)

### Rating Distribution by Bank

![Rating Distribution](images/rating_distribution.png)

### Theme Analysis

![Theme Analysis](images/theme_analysis.png)

### Satisfaction Trends Over Time

![Trends](images/satisfaction_trends.png)

---

## 🌐 Deployment

### Streamlit Cloud (Current)

The dashboard is deployed at: **[ethiopianbankreview.streamlit.app](https://ethiopianbankreview.streamlit.app/)**

**Deployment Steps:**
1. Push code to GitHub
2. Connect repository to [share.streamlit.io](https://share.streamlit.io)
3. Set main file path: `dashboard/app.py`
4. Deploy

### Docker (Optional)

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY dashboard/ ./dashboard/
COPY dashboard/requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501"]
```

```bash
# Build and run
docker build -t ethiopian-bank-reviews .
docker run -p 8501:8501 ethiopian-bank-reviews
```

### Docker Compose

```yaml
version: '3.8'
services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m "feat: add amazing feature"
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Commit Convention
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👥 Maintainers & Contact

| Name | Role | Contact |
|------|------|---------|
| **Filimon Hailemariam** | Project Lead | [![GitHub](https://img.shields.io/badge/GitHub-Filimon--H-black?logo=github)](https://github.com/Filimon-H) |

---

## 🙏 Acknowledgments

- [Google Play Scraper](https://github.com/JoMingyu/google-play-scraper) for review extraction
- [Hugging Face](https://huggingface.co/) for DistilBERT model
- [Streamlit](https://streamlit.io/) for dashboard framework
- 10 Academy for project guidance

---

<p align="center">
  Made with ❤️ for Ethiopian Banking Innovation
</p>
