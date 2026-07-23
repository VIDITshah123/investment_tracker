import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, Alert, SectorRank
from modules.dashboard.components.company_card import render_company_card

def show():
    st.title("🏠 PB Equity Intelligence Platform — Home")
    st.caption("AI-Powered Equity Research Terminal | Pratik Bohra Investment Framework")

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    active_cos = session.query(Company).filter(Company.is_active == True).all()
    scores = [session.query(Score).filter_by(company_id=c.id).order_by(Score.created_at.desc()).first() for c in active_cos]
    valid_scores = [s.pb_score for s in scores if s]

    avg_sc = round(sum(valid_scores)/len(valid_scores), 1) if valid_scores else 0.0
    top10_count = sum(1 for s in valid_scores if s >= 80)
    watchlist_count = sum(1 for s in valid_scores if 60 <= s < 80)
    avoid_count = sum(1 for s in valid_scores if s < 60)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Companies Tracked", len(active_cos))
    col2.metric("Average PB Score", f"{avg_sc} ⭐")
    col3.metric("Buy Candidates", top10_count, "Top Tier")
    col4.metric("Watchlist", watchlist_count)
    col5.metric("Avoid / Review", avoid_count, "-Low Score")

    st.markdown("---")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("🏆 Top Leaderboard")
        scored_pairs = []
        for c in active_cos:
            s = session.query(Score).filter_by(company_id=c.id).order_by(Score.created_at.desc()).first()
            if s:
                scored_pairs.append((c, s))
        scored_pairs.sort(key=lambda x: x[1].pb_score, reverse=True)

        for idx, (c, s) in enumerate(scored_pairs[:5], start=1):
            render_company_card(idx, c.company_name, c.nse_symbol, s.pb_score, c.sector)

    with col_right:
        st.subheader("📊 Sector Performance")
        sector_ranks = session.query(SectorRank).order_by(SectorRank.avg_score.desc()).all()
        if sector_ranks:
            df_sec = pd.DataFrame([{
                "Sector": sr.sector_name,
                "Avg Score": sr.avg_score,
                "Companies": sr.company_count
            } for sr in sector_ranks])
            
            fig = px.bar(df_sec, x="Avg Score", y="Sector", orientation="h", color="Avg Score",
                         color_continuous_scale="Viridis", text="Avg Score")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font={'color': '#F3F4F6'}, height=300, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🔔 Recent System Updates & Alerts")
    alerts = session.query(Alert).order_by(Alert.created_at.desc()).limit(5).all()
    if alerts:
        for a in alerts:
            st.info(f"**[{a.created_at.strftime('%H:%M | %d-%b')}]** {a.message}")
    else:
        st.write("No recent alerts.")
