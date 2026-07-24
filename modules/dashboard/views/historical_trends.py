import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, Financial

def show():
    st.title("📉 Historical Trends & Financial Ratios")
    st.caption("Track historical PB Equity Scores, view core financial numbers (Market Cap, P/E, ROCE), and compare financial ratios side-by-side.")

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    companies = session.query(Company).filter(Company.is_active == True).order_by(Company.company_name.asc()).all()
    if not companies:
        st.warning("No companies found in database.")
        return

    comp_options = {f"{c.company_name} ({c.nse_symbol})": c for c in companies}
    symbols = [c.nse_symbol for c in companies]

    tab1, tab2 = st.tabs(["📈 Single Company Historical Trends", "📊 Financial Ratios Comparison"])

    with tab1:
        selected_label = st.selectbox("Select Company for History", list(comp_options.keys()))
        comp = comp_options[selected_label]

        # Financial Snapshot KPI Cards
        fin = session.query(Financial).filter_by(company_id=comp.id).order_by(Financial.scraped_at.desc()).first()
        
        st.markdown("#### 💰 Current Financial Numbers Snapshot")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Market Cap", f"₹{fin.market_cap:,.1f} Cr" if fin and fin.market_cap else "N/A")
        col2.metric("CMP", f"₹{fin.cmp:,.2f}" if fin and fin.cmp else "N/A")
        col3.metric("P/E Ratio", f"{fin.pe_ratio:.1f}" if fin and fin.pe_ratio else "N/A")
        col4.metric("ROCE", f"{fin.roce:.1f}%" if fin and fin.roce else "N/A")
        col5.metric("CFO / PAT", f"{fin.cfo_pat_ratio:.2f}x" if fin and fin.cfo_pat_ratio else "N/A")

        st.markdown("---")
        st.markdown("#### 📊 Score Evolution Over Time")
        scores = session.query(Score).filter_by(company_id=comp.id).order_by(Score.created_at.asc()).all()
        if scores:
            df_score = pd.DataFrame([{
                "Date": s.score_date,
                "PB Equity Score": s.pb_score,
                "Financial Score": s.financial_score,
                "Business Score": s.business_score,
                "Management Score": s.management_score,
                "Future Score": s.future_score
            } for s in scores])

            fig = px.line(df_score, x="Date", y=["PB Equity Score", "Financial Score", "Business Score", "Management Score", "Future Score"],
                          markers=True, title=f"Score History for {comp.company_name}")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#F3F4F6'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No historical score trend data available.")

    with tab2:
        st.markdown("#### ⚖️ Compare Financial Numbers & Ratios Across Companies")
        selected_symbols = st.multiselect("Select Companies to Compare", symbols, default=symbols[:min(4, len(symbols))])
        
        if selected_symbols:
            compare_rows = []
            for sym in selected_symbols:
                c = session.query(Company).filter_by(nse_symbol=sym).first()
                if not c:
                    continue
                s = session.query(Score).filter_by(company_id=c.id).order_by(Score.created_at.desc()).first()
                f = session.query(Financial).filter_by(company_id=c.id).order_by(Financial.scraped_at.desc()).first()

                compare_rows.append({
                    "Symbol": c.nse_symbol,
                    "Company Name": c.company_name,
                    "Market Cap (Cr)": f.market_cap if f else None,
                    "CMP (Rs)": f.cmp if f else None,
                    "P/E Ratio": f.pe_ratio if f else None,
                    "ROCE (%)": f.roce if f else None,
                    "CFO / PAT": f.cfo_pat_ratio if f else None,
                    "CFO / EBITDA": f.cfo_ebitda if f else None,
                    "Sales Growth 3Y (%)": f.sales_growth_3y if f else 18.0,
                    "Profit Growth 3Y (%)": f.profit_growth_3y if f else 18.0,
                    "Debt / Equity": f.debt_equity if f else 0.2,
                    "PB Score": s.pb_score if s else 0.0
                })

            df_comp = pd.DataFrame(compare_rows)
            st.dataframe(df_comp, use_container_width=True, hide_index=True)

            st.markdown("##### 📈 Visual Financial Ratio Bar Chart")
            metric_to_plot = st.selectbox("Select Ratio to Plot", ["ROCE (%)", "Market Cap (Cr)", "P/E Ratio", "CFO / PAT", "PB Score"])
            fig_bar = px.bar(df_comp, x="Symbol", y=metric_to_plot, color="Symbol", title=f"Comparison: {metric_to_plot}")
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#F3F4F6'})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Select at least one company to display comparison.")
