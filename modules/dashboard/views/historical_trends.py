import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score

def show():
    st.title("📉 Historical Score Trends")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    companies = session.query(Company).filter(Company.is_active == True).all()
    symbols = [c.nse_symbol for c in companies]
    selected_sym = st.selectbox("Select Company to View History", symbols)

    comp = session.query(Company).filter_by(nse_symbol=selected_sym).first()
    if comp:
        scores = session.query(Score).filter_by(company_id=comp.id).order_by(Score.created_at.asc()).all()
        if scores:
            df = pd.DataFrame([{
                "Date": s.score_date,
                "PB Score": s.pb_score,
                "Financial": s.financial_score,
                "Business": s.business_score,
                "Management": s.management_score,
                "Future": s.future_score
            } for s in scores])

            fig = px.line(df, x="Date", y=["PB Score", "Financial", "Business", "Management", "Future"], markers=True, title=f"Score History for {comp.company_name}")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#F3F4F6'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No score history found for this company.")
