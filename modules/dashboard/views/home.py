import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

import streamlit as st

def show():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); padding: 35px; border-radius: 15px; border: 1px solid #3B82F6; margin-bottom: 25px; text-align: center;">
        <h1 style="color: #F9FAFB; margin-bottom: 10px; font-size: 36px;">👋 Welcome to PB Equity Intelligence Terminal</h1>
        <p style="color: #93C5FD; font-size: 18px; max-width: 800px; margin: 0 auto 15px auto;">
            Your personal AI-powered equity research terminal built on the <b>Pratik Bohra Investment Framework</b>.
        </p>
        <div style="display: flex; justify-content: center; gap: 15px; margin-top: 20px;">
            <span style="background-color: #1E293B; color: #60A5FA; padding: 8px 16px; border-radius: 20px; font-size: 14px; border: 1px solid #334155;">
                🔍 100-Point PB Score
            </span>
            <span style="background-color: #1E293B; color: #34D399; padding: 8px 16px; border-radius: 20px; font-size: 14px; border: 1px solid #334155;">
                ⚡ Real-Time Screener Sync
            </span>
            <span style="background-color: #1E293B; color: #FBBF24; padding: 8px 16px; border-radius: 20px; font-size: 14px; border: 1px solid #334155;">
                🎙️ Concall & AR Intelligence
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📌 Terminal Navigation Guide")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background-color: #1F2937; padding: 20px; border-radius: 10px; border: 1px solid #374151; height: 220px;">
            <h4 style="color: #60A5FA; margin-top: 0;">🏢 Research & Profiles</h4>
            <p style="color: #D1D5DB; font-size: 14px;">
                Explore all tracked companies in <b>Companies</b>, or view deep-dive sub-scores, investment thesis, and risks in <b>Company Profile</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background-color: #1F2937; padding: 20px; border-radius: 10px; border: 1px solid #374151; height: 220px;">
            <h4 style="color: #34D399; margin-top: 0;">🎙️ Concall & Rankings</h4>
            <p style="color: #D1D5DB; font-size: 14px;">
                Select company concall research in <b>Concall Research</b>, or view sortable multi-dimensional leaderboards in <b>Rankings</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background-color: #1F2937; padding: 20px; border-radius: 10px; border: 1px solid #374151; height: 220px;">
            <h4 style="color: #FBBF24; margin-top: 0;">💼 Portfolio & Trends</h4>
            <p style="color: #D1D5DB; font-size: 14px;">
                Review auto-generated 10% weighted buy candidates in <b>Portfolio</b>, or compare financial metrics & ratios over time in <b>Historical Trends</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **Getting Started:** Select any page from the sidebar menu on the left to begin your research session.")
