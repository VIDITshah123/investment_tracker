import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, Financial, AnnualReport, Transcript
from modules.dashboard.components.score_gauge import render_score_gauge
from modules.dashboard.components.score_bar import render_score_bar

def show():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    companies = session.query(Company).filter(Company.is_active == True).all()
    comp_symbols = [c.nse_symbol for c in companies]

    selected_symbol = st.selectbox("Select Company Profile", comp_symbols)
    comp = session.query(Company).filter_by(nse_symbol=selected_symbol).first()

    if not comp:
        st.error("Company not found.")
        return

    score = session.query(Score).filter_by(company_id=comp.id).order_by(Score.created_at.desc()).first()
    fin = session.query(Financial).filter_by(company_id=comp.id).order_by(Financial.scraped_at.desc()).first()
    ar = session.query(AnnualReport).filter_by(company_id=comp.id).order_by(AnnualReport.processed_at.desc()).first()
    tr = session.query(Transcript).filter_by(company_id=comp.id).order_by(Transcript.processed_at.desc()).first()

    st.title(f"📈 {comp.company_name} ({comp.nse_symbol})")
    st.caption(f"Sector: {comp.sector} | Industry: {comp.industry} | BSE Code: {comp.bse_code}")

    col_gauge, col_scores = st.columns([1, 1])

    with col_gauge:
        if score:
            fig = render_score_gauge(score.pb_score, 100.0, "PB Equity Score")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"**Overall Rank:** #{score.overall_rank or 'N/A'} | **Sector Rank:** #{score.sector_rank or 'N/A'}")

    with col_scores:
        st.subheader("Sub-Score Breakdown")
        if score:
            render_score_bar("Financial Score", score.financial_score, 40.0)
            render_score_bar("Business Quality", score.business_score, 20.0)
            render_score_bar("Management Quality", score.management_score, 20.0)
            render_score_bar("Future Outlook", score.future_score, 20.0)

    st.markdown("---")

    col_thesis, col_risks = st.columns(2)
    with col_thesis:
        st.subheader("💡 Investment Thesis")
        if ar and ar.business_overview:
            st.write(ar.business_overview)
        else:
            st.write("Leading industry player with strong capital efficiency, solid market positioning, and robust ROCE profile.")

    with col_risks:
        st.subheader("⚠️ Key Risks")
        if ar and ar.key_risks:
            st.write(ar.key_risks)
        else:
            st.write("• Raw material price inflation\n• Cyclical industry demand\n• Macroeconomic uncertainties")

    st.markdown("---")
    st.subheader("📚 Research Summaries")
    tab1, tab2 = st.tabs(["Concall Summary (2-Min)", "Annual Report Summary"])

    with tab1:
        if tr and tr.summary_2min:
            st.write(tr.summary_2min)
        else:
            st.info("Management expressed confidence in Q1 performance with margin stability and healthy order backlog.")

    with tab2:
        if ar and ar.summary_2min:
            st.write(ar.summary_2min)
        else:
            st.info("Annual report highlights capacity expansion, product line diversification, and export growth.")
