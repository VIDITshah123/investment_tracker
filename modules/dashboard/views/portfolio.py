import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, Portfolio

def show():
    st.title("💼 Portfolio Recommendations")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    items = session.query(Portfolio).all()
    rows = []
    for item in items:
        c = session.query(Company).filter_by(id=item.company_id).first()
        s = session.query(Score).filter_by(company_id=item.company_id).order_by(Score.created_at.desc()).first() if c else None
        if c:
            rows.append({
                "Portfolio Tier": item.portfolio_type,
                "Symbol": c.nse_symbol,
                "Company Name": c.company_name,
                "PB Score": s.pb_score if s else "N/A",
                "Suggested Weight": f"{item.suggested_weight}%",
                "Rationale": item.rationale
            })

    df = pd.DataFrame(rows)
    if not df.empty:
        tab1, tab2 = st.tabs(["Top 10 Portfolio", "Top 20 Portfolio"])
        with tab1:
            st.dataframe(df[df["Portfolio Tier"] == "Top 10"], use_container_width=True, hide_index=True)
        with tab2:
            st.dataframe(df[df["Portfolio Tier"] == "Top 20"], use_container_width=True, hide_index=True)
    else:
        st.info("No portfolio recommendations generated yet.")
