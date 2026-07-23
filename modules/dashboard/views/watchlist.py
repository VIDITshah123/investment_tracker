import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, Watchlist

def show():
    st.title("⭐ Watchlist")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    items = session.query(Watchlist).all()
    rows = []
    for item in items:
        c = session.query(Company).filter_by(id=item.company_id).first()
        s = session.query(Score).filter_by(company_id=item.company_id).order_by(Score.created_at.desc()).first() if c else None
        if c:
            rows.append({
                "Symbol": c.nse_symbol,
                "Company Name": c.company_name,
                "Current PB Score": s.pb_score if s else "N/A",
                "Target PB Score": item.target_pb_score,
                "Notes": item.notes,
                "Added At": item.added_at.strftime('%Y-%m-%d')
            })

    df = pd.DataFrame(rows)
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Watchlist is empty.")
