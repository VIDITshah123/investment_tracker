import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def build_detailed_pdf():
    pdf_filename = Path(__file__).resolve().parent.parent / "data" / "PBEIP_Detailed_Non_Technical_User_Guide.pdf"
    pdf_filename.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(pdf_filename),
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#111827"),
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2563EB"),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#374151"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=12,
        spaceAfter=3
    )

    story = []

    # Cover Header
    story.append(Paragraph("PB Equity Intelligence Platform (PBEIP)", title_style))
    story.append(Paragraph("<b>Complete & Detailed Non-Technical User Manual & System Guide</b><br/>A comprehensive guide explaining how your digital equity research terminal works, scores stocks, and constructs portfolios.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563EB"), spaceAfter=12))

    # SECTION 1: EXECUTIVE SUMMARY
    story.append(Paragraph("1. Executive Summary & Purpose", h1_style))
    story.append(Paragraph(
        "The <b>PB Equity Intelligence Platform (PBEIP)</b> is an intelligent, automated stock research terminal built specifically around the <b>Pratik Bohra Investment Framework</b>. "
        "Analyzing stocks manually requires hundreds of hours reading financial statements, tracking stock screener metrics, reading 100-page Annual Reports, and listening to quarterly earnings calls. "
        "PBEIP automates this entire process end-to-end.", body_style))
    story.append(Paragraph(
        "It acts as your <b>24/7 personal research analyst</b>: fetching qualifying companies, downloading their corporate disclosures, extracting key business insights via AI, scoring each company on a rigorous <b>100-Point Quality Framework</b>, and recommending an optimized Top 10 portfolio.", body_style))

    # SECTION 2: HOW QUALIFYING STOCKS ARE FOUND
    story.append(Paragraph("2. How Stocks Enter Your Universe (The Screener Gatekeeper)", h1_style))
    story.append(Paragraph(
        "PBEIP logs into your <b>Screener.in</b> account automatically using session security. Every morning, it runs your custom screening criteria to filter out fundamentally weak, unprofitable, or over-leveraged companies.", body_style))
    
    screener_rules = [
        [Paragraph("<b>Financial Metric</b>", body_style), Paragraph("<b>Screening Rule</b>", body_style), Paragraph("<b>Non-Technical Reason (Why It Matters)</b>", body_style)],
        [Paragraph("Capital Efficiency", body_style), Paragraph("ROCE & ROE > 15%", body_style), Paragraph("Guarantees the business generates high profits for every rupee invested.", body_style)],
        [Paragraph("Cash Flow Quality", body_style), Paragraph("CFO / PAT >= 60%", body_style), Paragraph("Confirms accounting profit is backed by real cash deposited in bank accounts.", body_style)],
        [Paragraph("Growth Velocity", body_style), Paragraph("3Y Sales & Profit Growth > 15%", body_style), Paragraph("Ensures the company is expanding sales and earnings consistently.", body_style)],
        [Paragraph("Solvency & Debt", body_style), Paragraph("Debt to Equity < 1.0", body_style), Paragraph("Protects your capital by excluding heavily indebted companies at risk of debt crisis.", body_style)],
        [Paragraph("Coverage Strength", body_style), Paragraph("Interest Coverage Ratio > 3.0", body_style), Paragraph("Ensures operating profits easily cover debt interest payments by at least 3x.", body_style)],
        [Paragraph("Owner Alignment", body_style), Paragraph("Promoter Holding >= 40-50%", body_style), Paragraph("Ensures company founders have strong financial skin in the game.", body_style)],
        [Paragraph("Valuation Guardrail", body_style), Paragraph("PEG Ratio > 0 & < 1.5", body_style), Paragraph("Prevents buying overhyped stocks trading at absurd valuations relative to growth.", body_style)]
    ]
    t_screener = Table(screener_rules, colWidths=[110, 130, 290])
    t_screener.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F3F4F6")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_screener)

    # SECTION 3: THE 100-POINT PB EQUITY SCORE BREAKDOWN
    story.append(Paragraph("3. The 100-Point PB Equity Scoring Formula", h1_style))
    story.append(Paragraph(
        "PBEIP evaluates every company across <b>4 Core Quality Pillars</b> totaling <b>100 Points</b>:", body_style))

    pillars_table = [
        [Paragraph("<b>Pillar</b>", body_style), Paragraph("<b>Weight</b>", body_style), Paragraph("<b>Detailed Evaluation Breakdown</b>", body_style)],
        [Paragraph("<b>1. Financial Health</b>", body_style), Paragraph("<b>40 Points</b>", body_style), Paragraph("<b>Quantitative Hard Metrics:</b><br/>• ROCE (Max 8 pts): Scale from >25% (8 pts) down to <5% (2 pts)<br/>• Cash Flow / PAT Ratio (Max 6 pts): >100% (6 pts), >80% (5 pts)<br/>• Cash Flow / EBITDA (Max 6 pts): >80% (6 pts), >60% (5 pts)<br/>• 3-Year Sales Growth (Max 5 pts) & Profit Growth (Max 5 pts)<br/>• Debt / Equity (Max 5 pts): <0.1 (5 pts), <0.3 (4 pts), <0.5 (3 pts)<br/>• Interest Coverage (Max 3 pts), Promoter Holding (1 pt), Div Yield (1 pt)", body_style)],
        [Paragraph("<b>2. Business Quality</b>", body_style), Paragraph("<b>20 Points</b>", body_style), Paragraph("<b>Qualitative Moat & Positioning:</b><br/>Evaluates market leadership, pricing power, customer concentration risk, entry barriers, and industry growth tailwinds from Annual Reports.", body_style)],
        [Paragraph("<b>3. Management Quality</b>", body_style), Paragraph("<b>20 Points</b>", body_style), Paragraph("<b>Integrity & Execution:</b><br/>Analyzes earnings call transcripts (concalls) for management guidance accuracy, capital allocation discipline, transparency, and past promises vs results.", body_style)],
        [Paragraph("<b>4. Future Outlook</b>", body_style), Paragraph("<b>20 Points</b>", body_style), Paragraph("<b>Growth Drivers & Expansion:</b><br/>Evaluates planned factory expansions (CAPEX), new export markets, product line additions, and revenue visibility over 2-3 years.", body_style)]
    ]
    t_pillars = Table(pillars_table, colWidths=[110, 65, 355])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_pillars)

    # SECTION 4: DOCUMENT COLLECTION & AI EXTRACTION
    story.append(Paragraph("4. Automated Document Collection & AI Brain", h1_style))
    story.append(Paragraph("PBEIP automates document research through four intelligent steps:", body_style))
    story.append(Paragraph("1. <b>IR Web Crawling:</b> Locates official Investor Relations pages and finds Annual Reports, Concall Transcripts, and Investor Decks.", bullet_style))
    story.append(Paragraph("2. <b>PDF Downloading & Deduplication:</b> Downloads files into organized folders (`data/SYMBOL/FY26/`) and uses SHA-256 security hashing to ensure duplicate files are never re-processed.", bullet_style))
    story.append(Paragraph("3. <b>AI Intelligent Text Extraction:</b> Extracts text using PyMuPDF and processes it through AI engines to identify capex numbers, risk statements, and management guidance.", bullet_style))
    story.append(Paragraph("4. <b>2-Minute Executive Summaries & Guidance Tracking:</b> Summarizes hour-long earnings calls into bullet points and tracks if management revises revenue targets downward across 3 consecutive quarters.", bullet_style))

    # SECTION 5: THE 12 TERMINAL SCREENS WALKTHROUGH
    story.append(Paragraph("5. Detailed Walkthrough of Your 12 Terminal Screens", h1_style))
    
    views_detail = [
        [Paragraph("<b>Screen View</b>", body_style), Paragraph("<b>Detailed Functionality & How To Use It</b>", body_style)],
        [Paragraph("🏠 <b>1. Home</b>", body_style), Paragraph("<b>Executive Cockpit:</b> Shows overall portfolio metrics (tracked companies, average PB score, buy count), the Leaderboard Top 5 companies, a horizontal sector performance bar chart, and recent system alerts.", body_style)],
        [Paragraph("🏢 <b>2. Companies</b>", body_style), Paragraph("<b>Universe Explorer:</b> Search any company by symbol/name or filter by sector. Displays a comprehensive table with live price, P/E ratio, market cap, and sub-score breakdowns.", body_style)],
        [Paragraph("📈 <b>3. Company Profile</b>", body_style), Paragraph("<b>Individual Deep-Dive:</b> Features a sleek 100-point Score Gauge chart, sub-score progress bars, business thesis, key risks, and tabs for 2-minute concall summaries and annual report breakdowns.", body_style)],
        [Paragraph("🏆 <b>4. Rankings</b>", body_style), Paragraph("<b>Multi-Dimensional Leaderboard:</b> Sort all companies by Overall Rank, Financial Score, Business Quality, Management Score, or Future Outlook.", body_style)],
        [Paragraph("🏭 <b>5. Sector View</b>", body_style), Paragraph("<b>Industry Comparison:</b> Shows sector score averages, company counts, and identifies the #1 ranked market leader within each sector.", body_style)],
        [Paragraph("📊 <b>6. Compare Companies</b>", body_style), Paragraph("<b>Head-to-Head Radar Comparison:</b> Select any two companies to plot a side-by-side Plotly radar chart comparing Financial, Business, Management, and Future scores.", body_style)],
        [Paragraph("⭐ <b>7. Watchlist</b>", body_style), Paragraph("<b>Potential Buy Monitor:</b> Tracks high-potential companies approaching the buy threshold (scores 60-79) with target scores and custom research notes.", body_style)],
        [Paragraph("💼 <b>8. Portfolio</b>", body_style), Paragraph("<b>Auto-Generated Allocation Engine:</b> Automatically places Top 10 ranked companies into an equal-weighted 10% buy portfolio, and Top 20 into a secondary list.", body_style)],
        [Paragraph("🤖 <b>9. AI Chat Assistant</b>", body_style), Paragraph("<b>Conversational Analyst:</b> Type natural language questions like <i>'Which company has the highest management score?'</i> or <i>'Compare MCX and Trent'</i>.", body_style)],
        [Paragraph("🔔 <b>10. Alerts</b>", body_style), Paragraph("<b>System Event Log:</b> Records critical notifications such as new companies entering your screen, score changes (±3 points), or guidance downward revisions.", body_style)],
        [Paragraph("📉 <b>11. Historical Trends</b>", body_style), Paragraph("<b>Score Progression Chart:</b> Interactive line chart tracking how a stock's PB Equity Score and sub-scores evolve over quarters.", body_style)],
        [Paragraph("⚙️ <b>12. Settings</b>", body_style), Paragraph("<b>Control Panel:</b> Displays database paths, Screener credentials status, and manual buttons to trigger universe sync, score recalculation, or portfolio rebalancing.", body_style)]
    ]
    t_vdetail = Table(views_detail, colWidths=[130, 380])
    t_vdetail.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F3F4F6")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_vdetail)

    # SECTION 6: PRACTICAL USER WORKFLOWS
    story.append(Paragraph("6. Practical Daily & Quarterly User Workflows", h1_style))
    story.append(Paragraph("<b>Workflow A: Evaluating a New Stock in Under 2 Minutes</b>", h2_style))
    story.append(Paragraph("1. Open the terminal at `http://localhost:8501` (or your deployed URL).", bullet_style))
    story.append(Paragraph("2. Navigate to 📈 <b>Company Profile</b> and select the company.", bullet_style))
    story.append(Paragraph("3. Check the <b>PB Equity Score Gauge</b> (Score >= 80 indicates Top Tier Buy Candidate).", bullet_style))
    story.append(Paragraph("4. Review the <b>Sub-Score Breakdown bars</b> to see if weakness lies in Financials, Business, or Management.", bullet_style))
    story.append(Paragraph("5. Read the <b>2-Minute Concall Summary</b> to understand recent earnings momentum and management comments.", bullet_style))

    story.append(Paragraph("<b>Workflow B: Quarterly Portfolio Rebalancing</b>", h2_style))
    story.append(Paragraph("1. When new quarterly earnings results arrive, navigate to ⚙️ <b>Settings</b>.", bullet_style))
    story.append(Paragraph("2. Click <b>🔄 Sync Screener Universe</b> and <b>📊 Recalculate PB Scores</b>.", bullet_style))
    story.append(Paragraph("3. Go to 💼 <b>Portfolio</b> to review the updated Top 10 companies with 10% equal target weights.", bullet_style))

    # SECTION 7: WEALTH PROTECTION & RISK MANAGEMENT
    story.append(Paragraph("7. Wealth Protection Rules (Why PBEIP Keeps You Safe)", h1_style))
    story.append(Paragraph("PBEIP enforces strict discipline by systematically eliminating emotional investing traps:", body_style))
    story.append(Paragraph("• <b>Eliminates Cash-Flow Mismatch:</b> Rejects companies showing paper profit without actual cash flow.", bullet_style))
    story.append(Paragraph("• <b>Eliminates Debt Crises:</b> Excludes high debt-to-equity companies regardless of story.", bullet_style))
    story.append(Paragraph("• <b>Eliminates Management Bluffing:</b> Tracks guidance revisions across quarters and penalizes broken promises.", bullet_style))
    story.append(Paragraph("• <b>Removes Emotional FOMO:</b> Relies 100% on verifiable data and objective scoring math.", bullet_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#9CA3AF"), spaceAfter=8))
    story.append(Paragraph("<i>PB Equity Intelligence Platform v1.0 — Comprehensive Executive User Manual</i>", ParagraphStyle('FooterText', parent=body_style, fontSize=8, textColor=colors.HexColor("#6B7280"), alignment=1)))

    doc.build(story)
    print(f"Successfully generated Detailed User Guide PDF at: {pdf_filename}")

if __name__ == "__main__":
    build_detailed_pdf()
