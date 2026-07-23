import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, Financial
from modules.dashboard.components.ranking_table import render_ranking_table

def show():
    st.title("🏢 Companies Universe")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    companies = session.query(Company).filter(Company.is_active == True).all()

    search = st.text_input("🔍 Search Company by Name or Symbol")
    sectors = list(set(c.sector for c in companies if c.sector))
    selected_sector = st.selectbox("Filter by Sector", ["All Sectors"] + sectors)

    table_data = []
    for c in companies:
        if search and search.lower() not in c.company_name.lower() and search.lower() not in c.nse_symbol.lower():
            continue
        if selected_sector != "All Sectors" and c.sector != selected_sector:
            continue

        s = session.query(Score).filter_by(company_id=c.id).order_by(Score.created_at.desc()).first()
        fin = session.query(Financial).filter_by(company_id=c.id).order_by(Financial.scraped_at.desc()).first()

        table_data.append({
            "Symbol": c.nse_symbol,
            "Company Name": c.company_name,
            "Sector": c.sector or "N/A",
            "PB Score": s.pb_score if s else 0.0,
            "Financial": s.financial_score if s else 0.0,
            "Business": s.business_score if s else 0.0,
            "Management": s.management_score if s else 0.0,
            "Future": s.future_score if s else 0.0,
            "CMP (Rs)": fin.cmp if fin else None,
            "P/E": fin.pe_ratio if fin else None,
            "Market Cap (Cr)": fin.market_cap if fin else None,
        })

    df = pd.DataFrame(table_data)
    if not df.empty:
        df = df.sort_values(by="PB Score", ascending=False)
        render_ranking_table(df)
    else:
        st.warning("No companies match the search criteria.")
