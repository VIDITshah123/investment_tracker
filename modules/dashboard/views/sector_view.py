import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, SectorRank

def show():
    st.title("🏭 Sector View")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    sectors = [sr.sector_name for sr in session.query(SectorRank).all()]
    if not sectors:
        companies = session.query(Company).filter(Company.is_active == True).all()
        sectors = list(set(c.sector for c in companies if c.sector))

    selected_sec = st.selectbox("Select Sector", sectors)
    st.subheader(f"Sector Breakdown: {selected_sec}")

    sec_comps = session.query(Company).filter(Company.sector == selected_sec, Company.is_active == True).all()
    rows = []
    for c in sec_comps:
        s = session.query(Score).filter_by(company_id=c.id).order_by(Score.created_at.desc()).first()
        rows.append({
            "Sector Rank": s.sector_rank if s else "N/A",
            "Symbol": c.nse_symbol,
            "Company Name": c.company_name,
            "PB Score": s.pb_score if s else 0.0,
            "Financial": s.financial_score if s else 0.0,
            "Management": s.management_score if s else 0.0
        })

    df = pd.DataFrame(rows).sort_values(by="PB Score", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)
