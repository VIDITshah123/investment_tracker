# PB Equity Intelligence Platform (PBEIP)
## Product Requirements Document (PRD)
**Version:** 1.0  
**Date:** July 2026  
**Author:** Pratik Bohra  
**Status:** Approved for Development

---

## 1. Executive Summary

PBEIP is a personal, AI-powered equity research terminal that automates the full research pipeline — from universe tracking to scoring, ranking, and portfolio construction — using Pratik Bohra's proprietary investment framework (the **PB Equity Score**). It replaces the daily manual workflow of opening Screener.in, company IR pages, BSE/NSE, annual reports, and concall transcripts with a single intelligent dashboard.

> **Vision:** A mini Bloomberg Terminal tailored to one investor's philosophy — not a generic screener.

---

## 2. Problem Statement

| Today's Pain | Size of Problem |
|---|---|
| 41 companies tracked manually | Grows as the universe expands |
| 4 concall transcripts/company/year | ~40 pages each → **6,500+ pages/year** |
| Multiple websites opened per research session | Screener.in + BSE + NSE + IR pages + PDFs |
| Rankings updated mentally/manually | Stale, subjective, inconsistent |
| Missing cross-quarter patterns | E.g., guidance drift over 3 quarters |
| No single source of truth | Data lives in spreadsheets, bookmarks, notes |

---

## 3. Goals & Success Metrics

### 3.1 Goals
1. Reduce time spent per company from 60+ minutes to under 5 minutes.
2. Automate 100% of document collection from official company IR pages.
3. Score every company on the PB Equity Framework automatically.
4. Surface insights humans routinely miss (guidance drift, margin trends, promoter changes).
5. Produce a defensible, data-backed portfolio recommendation at any point in time.

### 3.2 Success Metrics (Post-Launch)
| Metric | Target |
|---|---|
| Documents auto-downloaded without manual intervention | >= 95% success rate |
| AI summary generation time per document | < 3 minutes |
| PB Score accuracy vs. manual benchmark score | <= 5 points deviation |
| Dashboard load time | < 2 seconds |
| Ranking freshness | Updated within 24 hours of new data |

---

## 4. Users & Personas

### Primary User: Pratik Bohra (Solo Investor)
- PGDM student interested in equity research
- Maintains a personal investable universe of ~41 companies
- Follows a proprietary scoring framework
- Needs research depth without time cost
- Will use the platform daily for monitoring, quarterly for deep dives

### Future Users (v2+)
- Other retail investors with similar frameworks
- PGDM/MBA students building research portfolios

---

## 5. Scope

### In Scope (v1.0)
- [x] Screener.in universe synchronization
- [x] Company master with IR URL discovery
- [x] Automated document downloading (Annual Reports, Concalls, Quarterly Results, Presentations)
- [x] AI summarization of all document types
- [x] Financial Score Engine (40 points)
- [x] Business Score Engine (20 points)
- [x] Management Score Engine (20 points)
- [x] Future Score Engine (20 points)
- [x] PB Equity Score aggregation (100 points)
- [x] Multi-dimensional ranking (Overall, Sector, Industry, Financial, Business, Management)
- [x] Portfolio recommendations (Top 10, Top 20, Watchlist, Avoid)
- [x] Streamlit dashboard with all views
- [x] Automated scheduling (daily/weekly/quarterly)
- [x] AI Chat Assistant

### Out of Scope (v1.0)
- [ ] Real-time price feeds / live market data
- [ ] Multi-user accounts / authentication
- [ ] Mobile app
- [ ] Trading / brokerage integration
- [ ] Backtesting engine (planned for v2)

---

## 6. Feature Requirements

### 6.1 Universe Manager (Module 1)

**FR-1.1** System SHALL scrape the Screener.in universe URL daily.

**FR-1.2** System SHALL extract: Company Name, NSE Symbol, Sector, Industry, Market Cap, and key financial ratios from Screener.

**FR-1.3** System SHALL detect **new companies added** to the universe and trigger the full onboarding pipeline (master creation -> document download -> scoring).

**FR-1.4** System SHALL detect **removed companies** and flag them in the database without deleting historical data.

**FR-1.5** System SHALL log every universe change with a timestamp.

---

### 6.2 Company Master (Module 2)

**FR-2.1** For every company in the universe, the system SHALL automatically discover and store:
- Company Name
- Sector & Industry
- Official Website URL
- Investor Relations URL
- Screener.in URL
- BSE Code
- NSE Symbol

**FR-2.2** System SHALL use web search + heuristic URL matching to discover IR pages without manual input.

**FR-2.3** IR URLs SHALL be validated and updated automatically if they return 404 or redirect.

---

### 6.3 Document Collector (Module 3)

**FR-3.1** System SHALL automatically download the following document types from each company IR page:
- Annual Reports (PDF)
- Quarterly Results (PDF)
- Investor/Earnings Presentations (PDF/PPT)
- Concall Transcripts (PDF/HTML)
- Corporate Announcements (PDF)

**FR-3.2** Documents SHALL be stored under: data/{company_name}/{FY}/{Q1|Q2|Q3|Q4}/

**FR-3.3** System SHALL track document metadata: filename, download date, fiscal year, quarter, document type, file hash (to detect duplicates).

**FR-3.4** System SHALL avoid re-downloading already stored documents (deduplication by hash).

**FR-3.5** Download failure SHALL be logged and retried once within 24 hours.

---

### 6.4 AI Research Engine (Module 4)

#### Annual Report Analysis
**FR-4.1** System SHALL extract from each Annual Report:
- Business Overview
- Products & Services
- Customer Profile
- Geographic Presence
- Key Risks
- CapEx Plans
- Management Quality Indicators
- Competitive Positioning
- Moat Assessment
- Growth Drivers

#### Concall Transcript Analysis
**FR-4.2** System SHALL extract from each Concall Transcript:
- Revenue Drivers
- Margin Commentary
- Working Capital Commentary
- Debt Guidance
- Management Guidance (numerical where available)
- Capacity Expansion Plans
- Identified Risks
- Q&A Highlights
- Future Outlook

**FR-4.3** System SHALL generate a **2-minute summary** for every document, formatted for dashboard display.

**FR-4.4** System SHALL detect **cross-quarter guidance drift** (e.g., 3 consecutive quarters of downward guidance revision) and flag it as an alert.

**FR-4.5** All AI extractions SHALL be stored in the database with the source document reference and extraction timestamp.

---

### 6.5 Scoring Engine (Module 5)

#### Financial Score — 40 Points

| Metric | Max Points | Rationale |
|---|---|---|
| ROCE | 8 | Capital efficiency |
| CFO/PAT | 6 | Earnings quality |
| CFO/EBITDA | 6 | Cash conversion |
| Sales Growth (3Y CAGR) | 5 | Top-line momentum |
| Profit Growth (3Y CAGR) | 5 | Bottom-line momentum |
| Debt/Equity Ratio | 5 | Balance sheet health |
| Interest Coverage | 3 | Debt serviceability |
| Promoter Holding % | 1 | Alignment |
| Dividend Yield | 1 | Capital return |
| **Total** | **40** | |

**FR-5.2** Each metric SHALL have clearly defined score bands (e.g., ROCE > 25% = 8/8).

#### Business Quality Score — 20 Points
**FR-5.3** System SHALL use AI-extracted Annual Report data to score:
- Moat strength (0-5)
- Customer diversification (0-3)
- Industry tailwinds (0-4)
- Competition intensity (0-4)
- CapEx efficiency (0-4)

#### Management Score — 20 Points
**FR-5.4** System SHALL analyze the **last 4 concall transcripts** and score:
- Guidance accuracy / honesty (0-7)
- Capital allocation quality (0-5)
- Communication clarity (0-4)
- Execution track record (0-4)

#### Future Score — 20 Points
**FR-5.5** System SHALL evaluate:
- Expansion plans (0-5)
- Demand visibility (0-5)
- Capacity utilization (0-5)
- Industry outlook (0-5)

#### PB Equity Score — 100 Points
**FR-5.6** PB Score = Financial (40) + Business (20) + Management (20) + Future (20)

**FR-5.7** Scores SHALL be recalculated automatically after every new document ingestion.

**FR-5.8** Score history SHALL be maintained in the database with timestamps for trend analysis.

---

### 6.6 Ranking Engine (Module 6)

**FR-6.1** System SHALL generate and maintain the following rankings:
- Overall PB Score Ranking
- Sector Ranking (within sector)
- Industry Ranking (within industry)
- Financial Score Ranking
- Business Score Ranking
- Management Score Ranking

**FR-6.2** Rankings SHALL be sortable and filterable in the dashboard.

**FR-6.3** Ranking changes SHALL be logged with delta (+/-) and reason.

---

### 6.7 Portfolio Engine (Module 7)

**FR-7.1** System SHALL auto-generate:
- **Top 10 Portfolio** — highest PB Scores with acceptable valuation
- **Top 20 Portfolio** — extended buy list
- **Watchlist** — companies approaching buy threshold
- **Avoid List** — companies with significant score decline or red flags

**FR-7.2** Portfolio view SHALL include: Rank, PB Score, Expected Return (qualitative), Risk Level, Dividend.

**FR-7.3** System SHALL generate **Rebalance Recommendations** when a company ranking changes significantly (>5 ranks).

---

### 6.8 Dashboard (Module 8)

| Page | Key Elements |
|---|---|
| **Home** | Universe count, Avg PB Score, Buy/Watchlist/Avoid counts, Top 10 leaderboard, Sector heatmap, Recent updates |
| **Companies** | Sortable/filterable table with PB Score, sub-scores, rank, sector |
| **Company Profile** | PB Score gauge, sub-scores, Investment Thesis, Key Risks, Concall Summary, Annual Report Summary, Historical Score chart, Documents |
| **Rankings** | Full ranking table sortable by any dimension |
| **Sector View** | Companies within a sector with scores and averages |
| **Compare** | Side-by-side comparison of 2 companies across 4 score dimensions |
| **Watchlist** | Watchlist entries with rationale |
| **Portfolio** | Holdings, weights, PB Scores, rebalance suggestions |
| **AI Chat** | Natural language query interface |
| **Alerts** | Feed: new documents, score changes, new company in universe |
| **Historical Trends** | Score trend charts per company over time |
| **Settings** | API keys, schedules, score weightage customization |

---

### 6.9 Automation Scheduler (Module 9)

| Frequency | Tasks |
|---|---|
| **Daily** | Screener.in universe sync; new company detection |
| **Weekly** | IR page checks for new document uploads |
| **Quarterly** | Full document download sweep; AI re-analysis; score recalculation; ranking update |

**FR-9.2** All job runs SHALL be logged with success/failure status and duration.

**FR-9.3** Failures SHALL generate an Alert visible in the dashboard.

---

### 6.10 AI Chat Assistant (Module 10)

**FR-10.1** User SHALL be able to ask natural language questions:
- "Which company has the strongest management?"
- "Which companies improved margins this quarter?"
- "Compare KPIT vs Hitachi."
- "Why did Maruti's score fall?"
- "Which company entered the Screener this week?"

**FR-10.2** AI Assistant SHALL answer using the platform's own database, not external internet.

**FR-10.3** Responses SHALL cite the source document/quarter for every claim.

---

## 7. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Performance** | Dashboard loads in < 2s; AI summaries in < 3 min |
| **Reliability** | Scheduled jobs at 99%+ uptime; failures retried |
| **Scalability** | Supports 200+ companies without redesign |
| **Data Integrity** | No duplicate documents; versioned scores |
| **Security** | API keys in .env; no credentials in Git |
| **Maintainability** | Modular codebase; each module independently testable |
| **Portability** | Local (Windows) first; Docker-ready for VPS |

---

## 8. Database Schema

| Table | Purpose |
|---|---|
| `Companies` | Master company data, IR URLs, metadata |
| `Financials` | Scraped financial ratios per quarter/year |
| `Scores` | PB Score history with sub-scores and timestamps |
| `Transcripts` | Concall AI extractions per quarter |
| `AnnualReports` | Annual report AI extractions per FY |
| `Presentations` | Investor presentation summaries |
| `QuarterlyResults` | Quarterly results data and summaries |
| `ManagementNotes` | Management quote tracking across quarters |
| `SectorRank` | Sector-level aggregated scores |
| `Portfolio` | Portfolio composition and weights |
| `Watchlist` | Watchlist entries with rationale |
| `Logs` | System job logs, errors, download history |
| `Alerts` | User-facing alert feed |

---

## 9. Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.13+ |
| **Database** | SQLite (upgradeable to PostgreSQL) |
| **Web Scraping** | Playwright + BeautifulSoup + Requests |
| **AI/LLM** | OpenAI API (GPT-4o recommended) |
| **Dashboard** | Streamlit |
| **Charts** | Plotly |
| **Scheduling** | Python schedule library |
| **Environment** | python-dotenv |
| **Version Control** | Git + GitHub |
| **Deployment (v1)** | Local (Windows) |
| **Deployment (v2)** | Docker + VPS or Streamlit Cloud |

---

## 10. Development Phases

| Phase | Module | Description |
|---|---|---|
| 1 | Setup | Project structure, venv, Git, dependencies |
| 2 | Database | SQLite schema creation |
| 3 | Universe Manager | Screener.in sync + change detection |
| 4 | Company Master | IR URL discovery automation |
| 5 | Document Collector | Automated PDF/HTML downloading |
| 6 | AI Research Engine | Document reading, extraction, summarization |
| 7-10 | Scoring Engines | Financial, Business, Management, Future |
| 11 | PB Score + Ranking | Aggregation + all ranking dimensions |
| 12 | Portfolio Engine | Top 10/20, Watchlist, Avoid |
| 13 | Dashboard | All 12 pages in Streamlit |
| 14 | Automation | Scheduler setup + job management |
| 15 | AI Chat | Natural language query interface |
| 16 | Testing & Polish | End-to-end testing, error handling |

---

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Screener.in blocks scraper | High | Login session with cookies; rate-limit requests |
| Inconsistent IR page structures | High | Company-specific adapters + BSE/NSE fallback |
| OpenAI API costs | Medium | Batch processing; cache extracted content |
| PDF parsing failures | Medium | Multiple parsers (PyMuPDF, pdfplumber); OCR fallback |
| Scoring subjectivity | Medium | Explicit score bands documented in docs/ |
| SQLite performance at scale | Low | PostgreSQL-ready schema; indexed from Day 1 |

---

## 12. Open Questions

1. **Screener.in Authentication**: Does the universe URL require login?
2. **Score Band Definitions**: What are exact thresholds per metric?
3. **Management Score Weighting**: How to numerically quantify "guidance honesty"?
4. **Document Scope**: Download all available history, or only last 3 years?
5. **Alert Delivery**: Dashboard-only, or also email/WhatsApp?

---

*End of PRD v1.0*
