Perfect. If you're handing this to Antigravity, then they need a proper Software Requirements Document (SRD) rather than a list of setup tasks.


---

PB Equity Intelligence Platform (PBEIP)

Version 1.0 - Software Development Roadmap

Objective

Build an AI-powered equity research platform that automatically:

Reads my Screener.in universe

Tracks additions/removals

Downloads official company documents

Reads and summarizes documents using AI

Scores companies

Ranks companies

Builds watchlists

Creates a portfolio dashboard



---

PHASE 1 – Project Setup

Task 1

Create project architecture

PB-Equity-Platform

database/
data/
scripts/
dashboard/
reports/
config/
logs/
backups/
docs/
tests/

main.py
requirements.txt
README.md
.gitignore


---

Task 2

Install

Python 3.13+

VS Code

Git

SQLite



---

Task 3

Initialize Git Repository

git init


---

Task 4

Create Virtual Environment

python -m venv venv

Activate

Windows

venv\Scripts\activate


---

Task 5

Install Required Packages

requests

beautifulsoup4

lxml

selenium

playwright

pandas

numpy

openpyxl

sqlite3

sqlalchemy

streamlit

plotly

python-dotenv

schedule

tqdm

openai


---

PHASE 2 – Database

Create SQLite Database

Tables

Companies

Financials

Scores

Transcripts

AnnualReports

Presentations

QuarterlyResults

ManagementNotes

SectorRank

Portfolio

Watchlist

Logs


---

PHASE 3 – Screener Integration

Input

https://www.screener.in/screens/3776183/pratik-bohra/

Automation

Read

Company

NSE Symbol

Sector

Industry

Market Cap

Ratios


Automatically update database

Detect

New Company

Removed Company



---

PHASE 4 – Company Master

Automatically generate

Company

Sector

Industry

Official Website

Investor Relation URL

Screener URL

BSE Code

NSE Symbol


---

PHASE 5 – Document Downloader

Automatically download

Official Website

↓

Investor Relations

↓

Store

Annual Report

Quarterly Results

Investor Presentation

Concall Transcript

Corporate Announcement

Folder

data/

company_name/

FY26/

Q1/

Q2/

Q3/

Q4/


---

PHASE 6 – AI Reader

Read

Annual Report

↓

Extract

Business Overview

Products

Customers

Geography

Risks

CapEx

Management

Competition

Moat

Growth Drivers


Save

Database


---

Read

Concall Transcript

↓

Extract

Revenue Drivers

Margin Commentary

Working Capital

Debt

Guidance

Capacity Expansion

Risks

Q&A Highlights

Future Outlook



---

PHASE 7 – Financial Score Engine

Weightages

ROCE

CFO/PAT

CFO/EBITDA

PEG

PE

Sales Growth

Profit Growth

Debt

Interest Coverage

Promoter Holding

Dividend Yield

Financial Score

40 Marks


---

PHASE 8 – Business Score Engine

Read

Annual Report

Business Quality

20 Marks


---

PHASE 9 – Management Score

Read

Last 4 Concalls

Evaluate

Guidance

Honesty

Capital Allocation

Execution


20 Marks


---

PHASE 10 – Future Score

Evaluate

Expansion

Demand

Capacity

Industry Outlook


20 Marks


---

PHASE 11 – PB Equity Score

Financial

40

Management

20

Business

20

Future

20

------------

100


---

PHASE 12 – Ranking Engine

Generate

Overall Ranking

Sector Ranking

Industry Ranking

Financial Ranking

Business Ranking

Management Ranking


---

PHASE 13 – Portfolio

Generate

Top 10

Top 20

Watchlist

Avoid


---

PHASE 14 – Dashboard

Dashboard

Home

Companies

Company Profile

Rankings

Sector Comparison

Financial Comparison

Watchlist

Portfolio

Settings


---

Company Page

Financial Score

Management Score

Business Score

Future Score

PB Score

Investment Thesis

Key Risks

Latest Concall Summary

Annual Report Summary

Quarterly Changes

Historical Score

Documents


---

PHASE 15 – Automation

Daily

Check

Screener


Weekly

Check

Official Websites


Quarterly

Check

Results

Presentation

Transcript


Update

Database

Recalculate Scores

Update Rankings


---

PHASE 16 – AI Assistant

Ask

Which company has the strongest management?

Which company improved margins?

Which company entered the Screener this week?

Which company deserves Top 10?

Compare KPIT vs Hitachi.

Show companies with improving cash flow.



---

TECH STACK

Backend

Python


Database

SQLite (upgradeable to PostgreSQL)


Automation

Playwright

BeautifulSoup

Requests


AI

OpenAI API


Dashboard

Streamlit


Charts

Plotly


Deployment

Docker (optional)

GitHub

Streamlit Cloud / VPS (later)



---

One recommendation before development starts

Ask Antigravity to build this in modules, not as one large application. A good sequence is:

1. Universe Manager (Screener sync)


2. Document Collector (official IR downloads)


3. AI Research Engine (summaries and insights)


4. Scoring Engine (PB Equity Score)


5. Ranking Engine


6. Dashboard


7. Automation & Scheduling



This modular approach will make the platform easier to test, maintain, and extend as your investment framework evolves.

If we build this properly, the outcome will be much bigger than "a stock screener." You'll end up with your own AI-powered equity research platform.

1. Your own Bloomberg/Morningstar (focused on your investment style)

Instead of opening:

Screener.in

Company websites

BSE

NSE

Annual reports

Concall transcripts


You'll open one dashboard.

For every company you'll instantly see:

PB Equity Score

Sector Rank

Overall Rank

Financial Score

Management Score

Business Score

Future Score

Investment Thesis

Key Risks

Latest AI summary



---

2. No more reading hundreds of pages

Today:

41 companies

↓

4 concalls

↓

40 pages each

↓

6500+ pages/year

The platform reads everything.

You only read

2-minute summary


---

3. AI starts finding things humans miss

Example

KPIT

Quarter 1

Management says

> We expect margins around 18%.



Quarter 2

Management says

> Margin pressure continues.



Quarter 3

Management

> Margin recovery delayed.



The AI tells you

> Management has reduced guidance for three consecutive quarters.



That is very difficult to notice manually.


---

4. Dynamic Ranking

Today

You manually think

> "Hitachi seems good."



Tomorrow

Platform says

Hitachi

PB Score

95

↓

90

Reason

Debt increased

Margins declined

Management cautious

Ranking updates automatically.


---

5. Portfolio Builder

Instead of choosing stocks emotionally

Platform says

Top 10

↓

Best Financials

↓

Best Management

↓

Reasonable Valuation

↓

Suggested Allocation


---

6. Alerts

Instead of checking news

You receive

Sagility

Q1 Transcript uploaded

↓

AI Summary ready

Or

KPIT

Promoter increased holding

Or

GE Vernova

Order book highest ever


---

7. Historical Memory

Suppose

5 years later

You ask

> What has Maruti management consistently said about EVs?



AI compares

20 transcripts

and answers in seconds.


---

8. Backtesting

You can answer questions like

> If I bought only companies with PB Score above 90 over the last 10 years, what would the return have been?



That's how you validate whether your framework actually outperforms.


---

9. MBA & Career Value

This could become the strongest project on your résumé.

Instead of saying:

> "Interested in equity research."



You can demonstrate:

Designed a proprietary stock ranking framework.

Automated data collection from official company sources.

Built an AI-powered research system.

Created a quantitative and qualitative scoring engine.

Developed a portfolio recommendation dashboard.


That's a concrete project recruiters can discuss with you.


---

10. Long-term Compounding

Every quarter the system gets smarter because it accumulates more data.

After 3 years you could have:

150+ companies.

2,400+ transcript summaries.

Hundreds of annual report analyses.

Thousands of financial data points.

A complete history of PB Scores and rankings.


New companies won't start from zero—they'll be compared against years of historical data.


---

11. Your Personal Research Assistant

Eventually you could ask:

"Which companies have improving cash flow but falling valuations?"

"Which management teams consistently beat their guidance?"

"Show me companies with high ROCE, improving margins, and strong order books."

"Compare KPIT and Sagility based on the last four concalls."

"Which company should move into my portfolio this month?"


The platform would answer using your own database, not generic internet information.


---

One reality check

The quality of the platform will depend on how disciplined you are about the scoring model.

The automation can gather documents and summarize them reliably. The hardest part is designing a scoring system that reflects your investment philosophy and produces rankings that stand up over time.

If we build that scoring methodology carefully and test it against historical performance, you'll have a genuinely valuable research tool rather than just another stock tracker.

This is actually one of the most important design decisions. I wouldn't build it as a spreadsheet dashboard—I would build it as a professional equity research terminal.

Here's the layout I envision.


---

🏠 Dashboard Home

-------------------------------------------------------------
 PB Equity Intelligence Platform                06-Jul-2026
-------------------------------------------------------------

📊 Companies Tracked          41
⭐ Average PB Score           78.4
🟢 Buy Candidates             9
🟡 Watchlist                 18
🔴 Avoid                     14

-------------------------------------------------------------

🏆 Top 10 Companies

1. Hitachi Energy             95
2. KPIT Technologies          94
3. GE Vernova                 93
4. Maruti Suzuki              92
...

-------------------------------------------------------------

Sector Performance

Electrical Equipment    ★★★★★
IT Services             ★★★★☆
Healthcare              ★★★★☆
Retail                  ★★★☆☆

-------------------------------------------------------------

Recent Updates

✓ KPIT Q1 Transcript Analysed

✓ Hitachi Annual Report Updated

✓ Sagility PB Score +3

✓ New Company Entered Universe


---

📈 Company Profile

Click on KPIT Technologies

You see:

-----------------------------------------------------

KPIT Technologies

PB Equity Score

94 / 100

★★★★★

Overall Rank

#2

Sector Rank

#1

-----------------------------------------------------

Financial Score

38 / 40

Management

19 / 20

Business

18 / 20

Future

19 / 20

-----------------------------------------------------

Investment Thesis

Leading automotive software company benefiting from
global SDV and EV trends.

-----------------------------------------------------

Key Risks

• Customer concentration

• Currency fluctuations

• Slow EV adoption

-----------------------------------------------------

Latest Concall

Q1 FY27

Management Confidence

★★★★★

Guidance

Positive

Margins

Stable

Growth

Improving

-----------------------------------------------------


---

📊 Financial Page

Financial Score

40

██████████

ROCE

18/20

CFO/PAT

10/10

Debt

10/10

PEG

9/10

Growth

9/10


---

🎤 Concall Analysis

Q4 FY26

Positive

• Revenue guidance increased

• New OEM wins

• Margin expansion

Negative

• Hiring cost increased

• Europe slowdown

Management Confidence

9.5/10


---

📚 Annual Report

Business

Software

Moat

High

Competition

Medium

Customers

Diversified

Industry

Growing

CapEx

Low

Return on Capital

Excellent


---

🏆 Ranking Page

Rank

Company

PB Score

Financial

Management

Business

Future

Sector

You can sort by any column.


---

🏭 Sector Page

Click

Electrical Equipment

Hitachi

95

GE Vernova

93

Transrail

84

Average Sector Score

91


---

📊 Compare Companies

Example

KPIT vs Sagility

Financial

KPIT

38

Sagility

34

------------------

Management

19

17

------------------

Business

18

16

------------------

Future

19

18


---

📁 Documents

Every company

Annual Report

Investor Presentation

Concall

Quarterly Results

Credit Rating

Shareholding

Corporate Announcement

One click opens the document.


---

🤖 AI Chat

Instead of searching

You ask

Which companies have improving margins?

or

Compare KPIT and Hitachi.

or

Why did Maruti's score fall?


---

📈 Portfolio

Current Holdings

Weight

PB Score

Expected Return

Risk

Dividend

Rebalance Recommendation


---

🔔 Alerts

Today

Hitachi

Transcript Uploaded

KPIT

New Order

Lupin

FDA Approval

Maruti

PB Score +4


---

📉 Historical Trends

For every company, you could see:

PB Score over time.

Financial Score trend.

Management Score trend.

Quarterly changes.

Ranking history.



---

My recommendation

I would build it to feel like a mini Bloomberg Terminal for your investment style, not a generic dashboard. The key difference is that every score and insight is based on your PB Equity Framework, not a one-size-fits-all model.

The interface should let you answer, in seconds, questions that currently require opening multiple websites and reading dozens of documents. That would make it both a practical investing tool and a standout project to showcase during your PGDM and beyond.