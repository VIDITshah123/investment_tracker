import streamlit as st

def render_company_card(rank: int, name: str, symbol: str, pb_score: float, sector: str):
    st.markdown(f"""
    <div style="background-color: #1F2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin: 0; color: #F9FAFB;">#{rank} {name} ({symbol})</h4>
            <span style="background-color: #10B981; color: white; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                {pb_score} / 100
            </span>
        </div>
        <p style="margin: 5px 0 0 0; color: #9CA3AF; font-size: 13px;">Sector: {sector or 'N/A'}</p>
    </div>
    """, unsafe_allow_html=True)
