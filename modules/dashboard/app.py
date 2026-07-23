import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st

st.set_page_config(
    page_title="PB Equity Intelligence Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for dark sleek research terminal look
st.markdown("""
<style>
    .stApp {
        background-color: #111827;
        color: #F9FAFB;
    }
    .stSidebar {
        background-color: #1F2937;
    }
</style>
""", unsafe_allow_html=True)

from modules.dashboard.views import (
    home, companies, company_profile, rankings, sector_view,
    compare, watchlist, portfolio, ai_chat, alerts, historical_trends, settings
)

def main():
    st.sidebar.title("📌 PBEIP Terminal")
    st.sidebar.caption("PB Equity Intelligence Platform v1.0")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "🏢 Companies",
            "📈 Company Profile",
            "🏆 Rankings",
            "🏭 Sector View",
            "📊 Compare Companies",
            "⭐ Watchlist",
            "💼 Portfolio",
            "🤖 AI Chat",
            "🔔 Alerts",
            "📉 Historical Trends",
            "⚙️ Settings"
        ]
    )

    if page == "🏠 Home":
        home.show()
    elif page == "🏢 Companies":
        companies.show()
    elif page == "📈 Company Profile":
        company_profile.show()
    elif page == "🏆 Rankings":
        rankings.show()
    elif page == "🏭 Sector View":
        sector_view.show()
    elif page == "📊 Compare Companies":
        compare.show()
    elif page == "⭐ Watchlist":
        watchlist.show()
    elif page == "💼 Portfolio":
        portfolio.show()
    elif page == "🤖 AI Chat":
        ai_chat.show()
    elif page == "🔔 Alerts":
        alerts.show()
    elif page == "📉 Historical Trends":
        historical_trends.show()
    elif page == "⚙️ Settings":
        settings.show()

if __name__ == "__main__":
    main()
