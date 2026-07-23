# PB Equity Intelligence Platform (PBEIP)
## System Design Document
**Version:** 1.0  
**Date:** July 2026  
**Author:** Pratik Bohra  
**Status:** Approved for Development

---

## 1. Architecture Overview

PBEIP follows a **modular pipeline architecture** where each module is independently runnable and testable. Data flows in one direction: Collection -> Storage -> Processing -> Scoring -> Presentation.

```
+------------------+     +------------------+     +------------------+
|  Universe Manager|---->|  Document        |---->|  AI Research     |
|  (Screener Sync) |     |  Collector       |     |  Engine          |
+------------------+     +------------------+     +------------------+
                                                          |
                                                          v
+------------------+     +------------------+     +------------------+
|  Dashboard       |<----|  Ranking Engine  |<----|  Scoring Engine  |
|  (Streamlit)     |     |  + Portfolio     |     |  (PB Score)      |
+------------------+     +------------------+     +------------------+
        ^                                                  ^
        |                    +------------------+          |
        +--------------------|  Automation      |----------+
                             |  Scheduler       |
                             +------------------+
                                     ^
                             +------------------+
                             |  AI Chat         |
                             |  Assistant       |
                             +------------------+
```

**Central State:** SQLite database (`database/pbeip.db`) — all modules read/write through SQLAlchemy ORM.

---

## 2. Module Architecture

### 2.1 Module Map

```
PB-Equity-Platform/
|
|-- modules/
|   |-- universe_manager/
|   |   |-- screener_scraper.py       # Screener.in scraping
|   |   |-- change_detector.py        # New/removed company detection
|   |   |-- universe_sync.py          # Orchestrator
|   |
|   |-- company_master/
|   |   |-- ir_discovery.py           # IR URL finder
|   |   |-- bse_lookup.py             # BSE code lookup
|   |   |-- master_builder.py         # Orchestrator
|   |
|   |-- document_collector/
|   |   |-- ir_crawler.py             # IR page crawler
|   |   |-- pdf_downloader.py         # PDF download handler
|   |   |-- document_classifier.py    # Type detection (AR/Concall/Results)
|   |   |-- deduplicator.py           # Hash-based dedup
|   |   |-- collector_orchestrator.py
|   |
|   |-- ai_engine/
|   |   |-- pdf_extractor.py          # PDF -> text
|   |   |-- annual_report_reader.py   # AR extraction prompts
|   |   |-- concall_reader.py         # Concall extraction prompts
|   |   |-- guidance_tracker.py       # Cross-quarter drift detection
|   |   |-- summarizer.py             # 2-min summary generator
|   |   |-- ai_client.py              # OpenAI API wrapper
|   |
|   |-- scoring/
|   |   |-- financial_scorer.py       # 40-point financial engine
|   |   |-- business_scorer.py        # 20-point business engine
|   |   |-- management_scorer.py      # 20-point management engine
|   |   |-- future_scorer.py          # 20-point future engine
|   |   |-- pb_score_aggregator.py    # 100-point rollup
|   |   |-- score_bands.py            # Scoring thresholds config
|   |
|   |-- ranking/
|   |   |-- ranking_engine.py         # All ranking dimensions
|   |   |-- portfolio_engine.py       # Top10/20/Watchlist/Avoid
|   |
|   |-- dashboard/
|   |   |-- app.py                    # Streamlit entry point
|   |   |-- pages/
|   |   |   |-- home.py
|   |   |   |-- companies.py
|   |   |   |-- company_profile.py
|   |   |   |-- rankings.py
|   |   |   |-- sector_view.py
|   |   |   |-- compare.py
|   |   |   |-- watchlist.py
|   |   |   |-- portfolio.py
|   |   |   |-- ai_chat.py
|   |   |   |-- alerts.py
|   |   |   |-- historical_trends.py
|   |   |   |-- settings.py
|   |   |-- components/
|   |   |   |-- score_gauge.py
|   |   |   |-- score_bar.py
|   |   |   |-- company_card.py
|   |   |   |-- ranking_table.py
|   |
|   |-- automation/
|   |   |-- scheduler.py              # Job scheduler
|   |   |-- daily_jobs.py
|   |   |-- weekly_jobs.py
|   |   |-- quarterly_jobs.py
|   |   |-- job_logger.py
|   |
|   |-- ai_chat/
|       |-- chat_interface.py         # Streamlit chat UI
|       |-- query_router.py           # NL -> structured query
|       |-- context_builder.py        # DB context for LLM
|
|-- database/
|   |-- models.py                     # SQLAlchemy ORM models
|   |-- migrations/
|   |-- pbeip.db                      # SQLite database
|
|-- data/
|   |-- {company_name}/
|       |-- FY26/
|           |-- Q1/
|           |-- Q2/
|           |-- Q3/
|           |-- Q4/
|
|-- config/
|   |-- settings.py                   # App configuration
|   |-- score_bands.yaml              # Scoring thresholds
|   |-- company_adapters.yaml         # Company-specific IR crawl rules
|
|-- scripts/
|   |-- init_db.py                    # Database initialization
|   |-- seed_companies.py             # Seed initial universe
|   |-- run_pipeline.py               # Full pipeline run
|
|-- logs/
|-- backups/
|-- tests/
|-- docs/
|-- main.py                           # Entry point
|-- requirements.txt
|-- .env                              # Secrets (not in Git)
|-- .gitignore
```

---

## 3. Database Design

### 3.1 Entity Relationship Overview

```
Companies (1) ----> (N) Financials
Companies (1) ----> (N) Scores
Companies (1) ----> (N) Transcripts
Companies (1) ----> (N) AnnualReports
Companies (1) ----> (N) Presentations
Companies (1) ----> (N) QuarterlyResults
Companies (1) ----> (N) ManagementNotes
Companies (1) ----> (N) Watchlist
Sectors    (1) ----> (N) Companies
Sectors    (1) ----> (N) SectorRank
```

### 3.2 Table Schemas

#### Companies
```sql
CREATE TABLE companies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nse_symbol      TEXT UNIQUE NOT NULL,
    bse_code        TEXT,
    company_name    TEXT NOT NULL,
    sector          TEXT,
    industry        TEXT,
    official_url    TEXT,
    ir_url          TEXT,
    screener_url    TEXT,
    is_active       BOOLEAN DEFAULT TRUE,
    added_date      DATE,
    removed_date    DATE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Financials
```sql
CREATE TABLE financials (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER REFERENCES companies(id),
    fiscal_year     TEXT,          -- e.g., "FY26"
    quarter         TEXT,          -- e.g., "Q1", "Annual"
    roce            REAL,
    cfo_pat_ratio   REAL,
    cfo_ebitda      REAL,
    sales_growth_3y REAL,
    profit_growth_3y REAL,
    debt_equity     REAL,
    interest_coverage REAL,
    promoter_holding REAL,
    dividend_yield  REAL,
    market_cap      REAL,
    pe_ratio        REAL,
    peg_ratio       REAL,
    source          TEXT,          -- "screener" | "manual"
    scraped_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Scores
```sql
CREATE TABLE scores (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          INTEGER REFERENCES companies(id),
    score_date          DATE,
    financial_score     REAL,      -- /40
    business_score      REAL,      -- /20
    management_score    REAL,      -- /20
    future_score        REAL,      -- /20
    pb_score            REAL,      -- /100
    overall_rank        INTEGER,
    sector_rank         INTEGER,
    industry_rank       INTEGER,
    score_version       TEXT,      -- "v1.0" for methodology versioning
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_scores_company_date ON scores(company_id, score_date);
```

#### Transcripts
```sql
CREATE TABLE transcripts (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          INTEGER REFERENCES companies(id),
    fiscal_year         TEXT,
    quarter             TEXT,
    document_path       TEXT,
    revenue_drivers     TEXT,      -- JSON
    margin_commentary   TEXT,
    working_capital     TEXT,
    debt_guidance       TEXT,
    management_guidance TEXT,      -- JSON: {metric, value, direction}
    capacity_expansion  TEXT,
    risks               TEXT,      -- JSON list
    qa_highlights       TEXT,
    future_outlook      TEXT,
    summary_2min        TEXT,
    management_confidence_score REAL,
    processed_at        TIMESTAMP
);
```

#### AnnualReports
```sql
CREATE TABLE annual_reports (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          INTEGER REFERENCES companies(id),
    fiscal_year         TEXT,
    document_path       TEXT,
    business_overview   TEXT,
    products_services   TEXT,
    customer_profile    TEXT,
    geography           TEXT,
    key_risks           TEXT,      -- JSON list
    capex_plans         TEXT,
    management_quality  TEXT,
    competitive_position TEXT,
    moat_assessment     TEXT,      -- "High" | "Medium" | "Low"
    growth_drivers      TEXT,
    summary_2min        TEXT,
    processed_at        TIMESTAMP
);
```

#### ManagementNotes
```sql
CREATE TABLE management_notes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER REFERENCES companies(id),
    fiscal_year     TEXT,
    quarter         TEXT,
    metric          TEXT,          -- e.g., "margin_guidance"
    stated_value    TEXT,          -- e.g., "18%"
    direction       TEXT,          -- "up" | "down" | "stable"
    quote           TEXT,          -- exact quote from transcript
    source_doc_id   INTEGER        -- FK to transcripts.id
);
```

#### Logs
```sql
CREATE TABLE logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name    TEXT,
    status      TEXT,              -- "success" | "failure" | "partial"
    message     TEXT,
    duration_s  REAL,
    run_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Alerts
```sql
CREATE TABLE alerts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id  INTEGER REFERENCES companies(id),
    alert_type  TEXT,              -- "new_doc" | "score_change" | "new_company" | "guidance_drift"
    message     TEXT,
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Data Flow Diagrams

### 4.1 Daily Flow
```
[Scheduler: 8 AM Daily]
        |
        v
[Universe Manager]
  - Scrape Screener.in
  - Diff vs DB companies
  - New company? -> Trigger onboarding
  - Removed? -> Mark inactive
        |
        v
[Write to: companies, logs, alerts]
```

### 4.2 New Document Flow
```
[Weekly Scheduler / Manual Trigger]
        |
        v
[IR Crawler] -> Detect new PDFs on IR page
        |
        v
[PDF Downloader] -> Download to data/{company}/{FY}/{Q}/
        |
        v
[Deduplicator] -> Check hash; skip if exists
        |
        v
[Document Classifier] -> Identify type (AR / Concall / Results)
        |
        v
[AI Engine] -> Extract structured data from PDF
        |
        v
[Write to: transcripts / annual_reports / quarterly_results]
        |
        v
[Scoring Engine] -> Recalculate all 4 sub-scores
        |
        v
[Write to: scores]
        |
        v
[Ranking Engine] -> Update all rankings
        |
        v
[Alert Generator] -> "KPIT Q1 Transcript Analysed. PB Score: 94"
```

### 4.3 AI Chat Flow
```
[User Query: "Which companies improved margins?"]
        |
        v
[Query Router] -> Classify intent -> "margin_trend"
        |
        v
[Context Builder]
  - Fetch margin data from financials table
  - Fetch margin commentary from transcripts table
  - Last 4 quarters per company
        |
        v
[LLM Call] -> OpenAI GPT-4o with structured context
        |
        v
[Response with citations: "KPIT (Q4 FY26 transcript), Sagility (Q3 FY26 transcript)"]
```

---

## 5. Scoring Engine Design

### 5.1 Financial Score (40 points)

```python
# score_bands.yaml structure
financial:
  roce:
    max: 8
    bands:
      - {min: 25, score: 8}
      - {min: 20, score: 7}
      - {min: 15, score: 6}
      - {min: 10, score: 4}
      - {min: 5,  score: 2}
      - {min: 0,  score: 0}
  cfo_pat:
    max: 6
    bands:
      - {min: 1.0,  score: 6}
      - {min: 0.8,  score: 5}
      - {min: 0.6,  score: 3}
      - {min: 0.0,  score: 1}
  # ... (all metrics defined similarly)
```

### 5.2 AI-Based Scoring (Business / Management / Future)

```
System Prompt -> Role definition + scoring rubric
User Prompt  -> Structured extracted data from DB
Response     -> JSON: {score: X, reasoning: "...", flags: [...]}
```

Example prompt structure for Management Score:
```
You are an equity analyst scoring management quality for {company}.

Data:
- Q1 FY26 Guidance: Margins ~18%. Actual: 16.2%. Miss: -1.8%
- Q2 FY26 Guidance: Margin pressure continues. Actual: 15.8%. 
- Q3 FY26 Guidance: Margin recovery delayed.

Score on:
1. Guidance Accuracy (0-7): How often does management meet stated targets?
2. Capital Allocation (0-5): Evidence of disciplined investment decisions?
3. Communication Clarity (0-4): Clear, honest communication?
4. Execution Track Record (0-4): Do they deliver on operational plans?

Return JSON: {"guidance_accuracy": X, "capital_allocation": X, "communication": X, "execution": X, "total": X, "key_flags": [...]}
```

---

## 6. AI Engine Design

### 6.1 PDF Extraction Pipeline
```
PDF File
  |
  v
[PyMuPDF / pdfplumber] -> Raw text extraction
  |
  v
[Text Chunker] -> Split into chunks <= 4000 tokens
  |
  v
[Chunk Classifier] -> Which section? (MD&A / Risk Factors / Financials)
  |
  v
[Targeted Extraction Prompts] -> Per section
  |
  v
[JSON Response Aggregator] -> Merge chunk responses
  |
  v
[Store in DB]
```

### 6.2 Guidance Drift Detector
```python
def detect_guidance_drift(company_id, metric="margin_guidance", quarters=4):
    """
    Fetch last N quarters of management notes for a metric.
    If direction is "down" for 3+ consecutive quarters -> raise alert.
    """
    notes = ManagementNotes.query(company_id=company_id, metric=metric).last(quarters)
    streak = count_consecutive_direction(notes, "down")
    if streak >= 3:
        create_alert(company_id, "guidance_drift", 
                    f"{metric} revised down for {streak} consecutive quarters")
```

### 6.3 OpenAI Cost Controls
- All AI calls go through `ai_client.py` which enforces:
  - Input/output token logging per call
  - Monthly spend tracking
  - Cache layer: if document hash + prompt hash is already in DB -> return cached response
  - Batch queuing: multiple documents processed in off-peak hours

---

## 7. Web Scraping Design

### 7.1 Screener.in Scraper
- Use **Playwright** (headless Chromium) with authenticated session
- Login via stored credentials in `.env`
- Extract table data from the custom screen URL
- Rate limit: 2 requests/second; random delay 1-3s between pages

### 7.2 IR Page Crawler

**Challenge:** Every company has a different IR page structure.

**Solution:** Two-tier approach:
1. **Generic Crawler** — detects PDFs linked on the IR page using keyword matching (annual report, concall, transcript, presentation, results)
2. **Company Adapters** — `company_adapters.yaml` stores company-specific XPath/CSS selectors for companies where the generic crawler fails

```yaml
# company_adapters.yaml
KPIT:
  ir_url: "https://www.kpit.com/investors/"
  annual_report_selector: "a[href*='annual-report']"
  results_selector: ".investor-docs a"

HITACHIENERGY:
  ir_url: "https://www.hitachienergy.com/in/en/investors"
  use_bse_fallback: true
```

### 7.3 BSE/NSE Fallback
- If IR page crawling fails -> fall back to BSE XBRL filings API
- BSE provides structured quarterly results and announcements
- URL pattern: `https://api.bseindia.com/BseIndiaAPI/api/AnnSubPDFDoc/w?pdfname={filename}`

---

## 8. Dashboard Design

### 8.1 Streamlit Architecture
```
app.py
  |-- sidebar navigation
  |-- page router -> loads page module
  |-- shared state: st.session_state
       |-- selected_company
       |-- date_range
       |-- filters
```

### 8.2 Component Design

**Score Gauge** (`components/score_gauge.py`)
```python
def render_score_gauge(score: float, max_score: float, label: str):
    """Plotly indicator gauge colored by score bracket."""
    color = "green" if score/max_score > 0.8 else "orange" if score/max_score > 0.6 else "red"
    # Returns plotly figure
```

**Company Card** (`components/company_card.py`)
```
+----------------------------------+
| KPIT Technologies          Rank#2 |
| PB Score: 94/100  ★★★★★         |
| Sector: IT  |  Industry: Auto SW  |
| F:38 B:18 M:19 Fu:19             |
+----------------------------------+
```

### 8.3 Key Dashboard Pages

#### Home Page Layout
```
[ PB EQUITY INTELLIGENCE PLATFORM ]         [Date: 06-Jul-2026]

[Companies: 41] [Avg Score: 78.4] [Buy: 9] [Watch: 18] [Avoid: 14]

TOP 10                          SECTOR HEATMAP
1. Hitachi Energy   95          Electrical Equip  ████████░░ 91
2. KPIT Tech        94          IT Services       ███████░░░ 84
3. GE Vernova       93          Healthcare        ██████░░░░ 72
...

RECENT UPDATES
[✓] KPIT Q1 Transcript Analysed   [5 min ago]
[✓] Sagility PB Score +3          [1 hr ago]
[✓] New Company: XYZ entered      [Today]
```

---

## 9. Automation Scheduler Design

### 9.1 Job Definitions

```python
# automation/scheduler.py

import schedule

# Daily: 7:00 AM
schedule.every().day.at("07:00").do(run_universe_sync)

# Weekly: Monday 8:00 AM
schedule.every().monday.at("08:00").do(run_weekly_ir_check)

# Quarterly: Triggered manually or on date config
# (April 15, July 15, October 15, January 15)
schedule.every().day.at("09:00").do(check_quarterly_trigger)
```

### 9.2 Job Execution Pattern

```python
def run_job(job_name: str, job_fn: callable):
    start = time.time()
    try:
        job_fn()
        log_job(job_name, "success", duration=time.time()-start)
    except Exception as e:
        log_job(job_name, "failure", message=str(e))
        create_alert(None, "system", f"Job {job_name} failed: {e}")
```

---

## 10. AI Chat Design

### 10.1 Query Classification

| Intent | Example Query | Resolution |
|---|---|---|
| `score_query` | "Which company has the best management score?" | DB query: SELECT MAX(management_score) |
| `comparison` | "Compare KPIT vs Hitachi" | Fetch both company profiles from DB |
| `trend_query` | "Which companies improved margins?" | Compare financials across last 2 quarters |
| `document_query` | "What did KPIT say about EV in Q1?" | Semantic search in transcripts table |
| `portfolio_query` | "Which company should enter Top 10?" | Portfolio engine re-evaluation |
| `alert_summary` | "What changed this week?" | Fetch recent alerts |

### 10.2 Context Window Management

```python
def build_context(intent, entities):
    if intent == "comparison":
        return {
            "company_a": fetch_full_profile(entities[0]),
            "company_b": fetch_full_profile(entities[1]),
            "instruction": "Compare these two companies across all 4 score dimensions. Be specific and cite quarters."
        }
```

---

## 11. Security Design

| Concern | Approach |
|---|---|
| API Keys | Stored only in `.env`; loaded via `python-dotenv`; `.env` in `.gitignore` |
| Screener Credentials | Same `.env` pattern |
| No public exposure | Local-only in v1; no authentication needed |
| Data backups | Weekly SQLite backup to `backups/` directory |
| Rate limiting | All scrapers have configurable delay and retry limits |

---

## 12. Testing Strategy

### 12.1 Test Structure
```
tests/
|-- unit/
|   |-- test_financial_scorer.py    # Test score band calculations
|   |-- test_deduplicator.py        # Test hash-based dedup
|   |-- test_guidance_tracker.py    # Test drift detection
|
|-- integration/
|   |-- test_pipeline.py            # Full pipeline with mock data
|   |-- test_db_operations.py       # CRUD operations
|
|-- fixtures/
    |-- sample_transcript.pdf
    |-- sample_annual_report.pdf
    |-- mock_screener_response.json
```

### 12.2 Testing Approach
- **Unit tests**: `pytest` for all scoring functions with known inputs/expected outputs
- **Integration tests**: Full pipeline run on a single test company with local PDF fixtures
- **Score validation**: Compare AI-generated scores against manually scored benchmarks for 5 companies

---

## 13. Deployment (Local — Windows Only)

> **Note:** This platform is built for local use. No Docker, no cloud, no server required.

### 13.1 First-Time Setup
```powershell
# 1. Open the project folder
cd C:\PB-Equity-Platform

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate

# 4. Install all dependencies
pip install -r requirements.txt

# 5. Set up environment variables
copy .env.example .env
# Open .env and fill in: OPENAI_API_KEY, SCREENER_EMAIL, SCREENER_PASSWORD

# 6. Initialize the database
python scripts/init_db.py

# 7. Seed initial company universe
python scripts/seed_companies.py
```

### 13.2 Running the Platform
```powershell
# Full platform (dashboard + scheduler together)
python main.py

# Dashboard only
streamlit run modules/dashboard/app.py

# Scheduler only (runs in background, picks up job times from config)
python main.py --scheduler

# Manual one-off pipeline run
python scripts/run_pipeline.py --company KPIT
python scripts/run_pipeline.py --all
```

### 13.3 Daily Usage Pattern
```
Every Morning:
  - Scheduler auto-ran at 7:00 AM (universe sync + IR check)
  - Open browser -> http://localhost:8501
  - Check Alerts page for overnight updates
  - Read new AI summaries

Results Season (Quarterly):
  - python scripts/run_pipeline.py --all
  - All documents downloaded, analysed, scored, ranked automatically
  - Check Rankings and Portfolio pages for changes
```

### 13.4 Updating the Platform
```powershell
# Pull latest code
git pull origin main

# Re-install any new dependencies
pip install -r requirements.txt

# Run any DB migrations
python scripts/migrate_db.py
```

---

## 14. Performance Considerations

| Concern | Solution |
|---|---|
| Large number of companies | Paginated DB queries; Streamlit caching with `@st.cache_data` |
| AI call latency | Async batch processing; pre-compute summaries; cache in DB |
| PDF parsing large files | Stream PDF pages; process in chunks |
| SQLite write contention | WAL mode enabled; single writer pattern |
| Dashboard responsiveness | Pre-compute ranking tables nightly; serve from DB |

```python
# Enable WAL mode for SQLite
engine = create_engine("sqlite:///database/pbeip.db")
with engine.connect() as conn:
    conn.execute(text("PRAGMA journal_mode=WAL"))
```

---

## 15. Full Version Roadmap (v1.0 → v4.0)

> All versions are planned upfront. Each builds directly on the previous with no breaking changes.

---

### Version 1.0 — Core Platform *(Months 1–3)*
**Goal:** Working end-to-end pipeline. Screener sync → Documents → AI extraction → PB Score → Dashboard.

| Module | What Gets Built |
|---|---|
| Universe Manager | Screener.in sync, new/removed company detection, daily scheduling |
| Company Master | IR URL auto-discovery, BSE/NSE code lookup |
| Document Collector | Annual Reports, Concalls, Quarterly Results, Presentations — auto-downloaded |
| AI Research Engine | Annual Report: 10-field extraction. Concall: 9-field extraction. 2-min summaries for every doc |
| Financial Scorer | 40-point scoring across 9 financial metrics with explicit score bands |
| Business Scorer | 20-point AI-driven quality score sourced from Annual Reports |
| Management Scorer | 20-point score from last 4 concall transcripts |
| Future Scorer | 20-point score from expansion/demand/capacity/outlook data |
| PB Score Engine | 100-point aggregation + full score history maintained |
| Ranking Engine | Overall, Sector, Industry, Financial, Business, Management rankings |
| Portfolio Engine | Top 10, Top 20, Watchlist, Avoid — auto-generated |
| Dashboard | 12 pages: Home, Companies, Profile, Rankings, Sector, Compare, Watchlist, Portfolio, AI Chat, Alerts, History, Settings |
| Scheduler | Daily (universe), Weekly (IR check), Quarterly (full pipeline) |
| AI Chat | Natural language queries answered from local DB |

**Stack at v1.0:** Python 3.13 · SQLite · Playwright · GPT-4o API · Streamlit · Plotly

---

### Version 1.5 — Hardening & Polish *(Month 4)*
**Goal:** Make v1.0 rock-solid for daily use. Fix all friction points discovered in real usage.

| Area | What Changes |
|---|---|
| Scraping Resilience | Company-specific IR adapter YAML for stubborn IR pages; BSE XBRL fallback |
| Error Recovery | Auto-retry on failed downloads; partial pipeline re-run without full reset |
| Guidance Drift Detector | Cross-quarter tracker: flag 3+ consecutive guidance misses as a red alert |
| Score Audit Trail | Every score shows which document version it was computed from |
| Dashboard Polish | Score gauges, colour-coded tables, score delta badges ("+3 this quarter") |
| Alerts System | Rich alert feed: new document, score changed, new company, guidance drift |
| Data Validation | Sanity checks before scoring: flag missing or incomplete data |
| Backup System | Automated weekly SQLite backup to `backups/` with timestamp |

**No new modules — all improvements to v1.0 modules.**

---

### Version 2.0 — Intelligence Upgrade *(Months 5–7)*
**Goal:** The platform starts finding things humans consistently miss. Deeper AI, semantic search, backtesting.

| Feature | Description |
|---|---|
| **Vector Search** | Embed all transcript + annual report text into a local vector store (ChromaDB). Enables: "What has KPIT said about SDV over the last 3 years?" — answers in seconds from 20+ documents |
| **Backtesting Engine** | Track historical PB Scores vs. actual stock price returns. Answer: "If I held only companies with PB Score above 85, what was the return over 3 years?" Validates the framework quantitatively |
| **WhatsApp / Email Alerts** | Push alerts via Twilio WhatsApp API or SMTP email: new document ready, score changes ±5, new company enters universe — no need to open the dashboard |
| **Guidance Accuracy Tracker** | Auto-compare management's stated guidance vs. actual quarterly results. Honesty score per company tracked over 8 quarters |
| **Multi-Quarter Trend Charts** | 8-quarter trend for every financial metric per company. Visualise ROCE, margins, cash flow all in one view |
| **Sector Intelligence** | Sector-level AI insight: "Electrical Equipment sector: order book accelerating across 3 of 4 companies this quarter" |
| **Comparative AI Reports** | On-demand: full AI-written comparison report for any 2 companies with source citations per quarter |
| **Score Simulation** | "What would KPIT's PB Score be if ROCE fell to 12%?" Sensitivity analysis on the scoring model |

**New additions:** ChromaDB (vector store), `yfinance` (price history), Twilio (push alerts)  
**Stack at v2.0:** SQLite + ChromaDB · GPT-4o + text-embedding-3-small · Streamlit

---

### Version 3.0 — Scale & Institutional Memory *(Months 8–12)*
**Goal:** Platform accumulates deep, compounding memory. Becomes more valuable the longer it runs.

| Feature | Description |
|---|---|
| **PostgreSQL Migration** | Migrate from SQLite when universe exceeds 150 companies or queries slow down. Full migration script + zero data loss |
| **Historical Memory Engine** | 5-year memory per company: every score, every management statement, every guidance number — stored and queryable. "What has Maruti said about EVs across 20 transcripts?" |
| **Universe Expansion** | Support 200+ companies without redesign. Batch AI processing with priority queue — results season companies processed first |
| **Management Statement Database** | Dedicated table tracking every forward-looking statement with actual-vs-stated outcome logged per quarter. The most powerful accountability tool in the platform |
| **Research Report Generator** | Auto-generate a 2-page PDF research note per company: Investment Thesis, Key Risks, Score Breakdown, Concall Highlights, Recommendation. Ready to share or present |
| **Watchlist Intelligence** | AI monitors watchlist companies and alerts when a score crosses the buy threshold with the exact reason (which metric improved, which document triggered it) |
| **Portfolio Rebalance Engine** | Monthly engine: identify companies to exit (score fell below floor) and candidates to enter (score crossed ceiling). Rule-based, not emotional |

**New additions:** PostgreSQL (`psycopg2`), ReportLab (PDF report generation)  
**Stack at v3.0:** PostgreSQL + ChromaDB · GPT-4o + Embeddings · Streamlit

---

### Version 4.0 — AI-Native Research Terminal *(Year 2+)*
**Goal:** The platform rivals a junior equity analyst in analytical depth and speed.

| Feature | Description |
|---|---|
| **Fine-tuned LLM** | Fine-tune a smaller open-source model (Mistral 7B or LLaMA 3) on Indian equity documents — concall transcripts, SEBI filings, annual reports. Lower cost per call, higher domain accuracy |
| **Real-time Price Integration** | NSE/BSE live price feeds via broker API or NSE Python. PB Score combined with live valuation (PE, Market Cap) for buy/sell signal generation |
| **Multi-user Support** | Basic auth layer for 2-3 trusted users (investment club). Shared universe, separate watchlists and portfolios per user |
| **FastAPI Backend** | REST API wrapping the scoring engine: programmatic score queries, potential Excel plugin, future mobile app backend |
| **Mobile Dashboard** | React Native or Streamlit Mobile app. Morning briefing: top movers, new documents, alerts — at a glance on phone |
| **Self-curating Universe** | Platform auto-detects companies qualifying for the universe based on user-defined filters (ROCE > 15%, Market Cap > 1000 Cr). Universe adds candidates automatically |
| **Peer Comparison Engine** | For any company, auto-identify the 5 most comparable peers (sector, size, business model) and show a structured side-by-side comparison |
| **Investment Thesis Generator** | AI generates a full structured thesis: Bull Case, Bear Case, Key Catalysts, Key Risks, Entry Price Range, Target Price (qualitative), 12-month outlook |

**Stack at v4.0:**
```
Fine-tuned Mistral/LLaMA + OpenAI GPT-4o (hybrid routing)
PostgreSQL + ChromaDB
FastAPI backend + Streamlit frontend
NSE/BSE live price feed
Multi-user auth (JWT)
React Native mobile app
```

---

### Version Summary

| Version | Timeline | Key Theme | Universe Size | Database | AI |
|---|---|---|---|---|---|
| **v1.0** | Month 1–3 | Core pipeline working | ~41 | SQLite | GPT-4o API |
| **v1.5** | Month 4 | Stable for daily use | ~41–60 | SQLite | GPT-4o API |
| **v2.0** | Month 5–7 | Semantic search + Backtesting | ~60–100 | SQLite + ChromaDB | GPT-4o + Embeddings |
| **v3.0** | Month 8–12 | Scale + Institutional memory | ~100–200 | PostgreSQL | GPT-4o + Embeddings |
| **v4.0** | Year 2+ | AI-native terminal | 200+ | PostgreSQL + ChromaDB | Fine-tuned + GPT-4o |

---

*End of System Design v1.0*
