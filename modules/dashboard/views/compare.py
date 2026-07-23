import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score

def show():
    st.title("📊 Compare Companies")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    companies = session.query(Company).filter(Company.is_active == True).all()
    symbols = [c.nse_symbol for c in companies]

    col1, col2 = st.columns(2)
    with col1:
        comp1_sym = st.selectbox("Company 1", symbols, index=0)
    with col2:
        comp2_sym = st.selectbox("Company 2", symbols, index=min(1, len(symbols)-1))

    c1 = session.query(Company).filter_by(nse_symbol=comp1_sym).first()
    c2 = session.query(Company).filter_by(nse_symbol=comp2_sym).first()

    s1 = session.query(Score).filter_by(company_id=c1.id).order_by(Score.created_at.desc()).first() if c1 else None
    s2 = session.query(Score).filter_by(company_id=c2.id).order_by(Score.created_at.desc()).first() if c2 else None

    if s1 and s2:
        categories = ['Financial (/40)', 'Business (/20)', 'Management (/20)', 'Future (/20)']
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[s1.financial_score, s1.business_score, s1.management_score, s1.future_score],
            theta=categories,
            fill='toself',
            name=c1.company_name
        ))
        fig.add_trace(go.Scatterpolar(
            r=[s2.financial_score, s2.business_score, s2.management_score, s2.future_score],
            theta=categories,
            fill='toself',
            name=c2.company_name
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 40])),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#F3F4F6'}
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Side-by-Side Comparison")
        comp_df = pd.DataFrame({
            "Metric": ["PB Score", "Financial Score", "Business Score", "Management Score", "Future Score"],
            c1.company_name: [s1.pb_score, s1.financial_score, s1.business_score, s1.management_score, s1.future_score],
            c2.company_name: [s2.pb_score, s2.financial_score, s2.business_score, s2.management_score, s2.future_score],
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)
