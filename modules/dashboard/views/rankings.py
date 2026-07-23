import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score
from modules.dashboard.components.ranking_table import render_ranking_table

def show():
    st.title("🏆 Multi-Dimensional Rankings")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    companies = session.query(Company).filter(Company.is_active == True).all()
    rows = []
    for c in companies:
        s = session.query(Score).filter_by(company_id=c.id).order_by(Score.created_at.desc()).first()
        if s:
            rows.append({
                "Rank": s.overall_rank or 999,
                "Symbol": c.nse_symbol,
                "Company Name": c.company_name,
                "Sector": c.sector or "N/A",
                "PB Score": s.pb_score,
                "Financial": s.financial_score,
                "Business": s.business_score,
                "Management": s.management_score,
                "Future": s.future_score,
            })

    df = pd.DataFrame(rows)
    if not df.empty:
        sort_col = st.selectbox("Sort Rankings By", ["Overall Rank", "PB Score", "Financial", "Business", "Management", "Future"])
        if sort_col == "Overall Rank":
            df = df.sort_values(by="Rank", ascending=True)
        else:
            df = df.sort_values(by=sort_col, ascending=False)

        render_ranking_table(df)
