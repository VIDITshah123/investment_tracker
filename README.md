# PB Equity Intelligence Platform (PBEIP)

An AI-powered personal equity research terminal that automates company universe tracking, official document collection, AI summarization, scoring, ranking, and portfolio construction using a proprietary investment framework (**PB Equity Score**).

---

## 🌟 Key Features

- **Automated Screener.in Sync**: Daily automated scraping of custom Screener screens with session authentication.
- **Company Master & IR Discovery**: Automatic discovery of official IR URLs, BSE codes, and NSE symbols.
- **Automated Document Collection**: PDF downloading for Annual Reports, Concall Transcripts, Presentations, and Quarterly Results.
- **AI Research Engine**: Structured 10-field extraction from Annual Reports & 9-field extraction from Concalls with 2-minute summaries.
- **PB Equity Scoring Engine (100 Points)**:
  - **Financial Score** (40 Points): ROCE, CFO/PAT, CFO/EBITDA, 3Y Sales Growth, 3Y Profit Growth, Debt/Equity, Interest Coverage, Promoter Holding, Dividend Yield.
  - **Business Quality Score** (20 Points): Moat, diversification, industry tailwinds.
  - **Management Quality Score** (20 Points): Guidance accuracy, capital allocation, execution.
  - **Future Outlook Score** (20 Points): Capacity expansion, demand visibility.
- **Multi-Dimensional Ranking Engine**: Overall, Sector, Industry, Financial, Business, Management rankings.
- **Portfolio & Watchlist Engine**: Auto-generates Top 10 (10% target weights), Top 20, Watchlist, and Avoid lists.
- **Interactive Research Terminal (Streamlit)**: 12 views including Home, Profile, Compare Radar, Rankings, AI Chat, Alerts, Trends, Settings.

---

## 🚀 Quick Start (Local Windows)

### 1. Clone & Setup Environment
```powershell
cd PB-Equity-Platform

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```env
OPENAI_API_KEY=your_openai_api_key_here
HF_TOKEN=your_huggingface_token_here
SCREENER_EMAIL=your_screener_email@example.com
SCREENER_PASSWORD=your_screener_password
SCREENER_URL=https://www.screener.in/screens/3776183/pratik-bohra/
```

### 3. Initialize & Seed Database
```powershell
venv\Scripts\python scripts/init_db.py
venv\Scripts\python scripts/seed_companies.py
venv\Scripts\python modules/scoring/pb_score_aggregator.py
venv\Scripts\python modules/ranking/ranking_engine.py
venv\Scripts\python modules/ranking/portfolio_engine.py
```

### 4. Launch Research Terminal
```powershell
venv\Scripts\python main.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 📂 Architecture Overview

```
PB-Equity-Platform/
├── config/              # App settings, score bands, company adapters
├── database/            # SQLAlchemy ORM models & SQLite database
├── docs/                # PRD.md & SYSTEM_DESIGN.md
├── modules/
│   ├── universe_manager/# Screener scraper & sync engine
│   ├── company_master/  # IR URL & BSE lookup
│   ├── document_collector/ # PDF crawlers & downloader
│   ├── ai_engine/       # AI extractions & summarizer
│   ├── scoring/         # Financial & qualitative scorers
│   ├── ranking/         # Multi-dimensional ranking & portfolio engine
│   ├── dashboard/       # Streamlit terminal app & views
│   ├── automation/      # Daily & quarterly scheduler
│   └── ai_chat/         # Natural language research assistant
├── scripts/             # DB init & seed scripts
├── main.py              # Application entry point
├── requirements.txt
└── .gitignore
```

---

## 📄 Documentation

- [Product Requirements Document (PRD.md)](docs/PRD.md)
- [System Design Document (SYSTEM_DESIGN.md)](docs/SYSTEM_DESIGN.md)

---

## 🔒 Security
Your API keys, Screener credentials, local database (`pbeip.db`), and downloaded documents are excluded from Git via `.gitignore`.
