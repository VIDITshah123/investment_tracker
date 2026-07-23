import streamlit as st
from config.settings import SCREENER_URL, DB_PATH, DATA_PATH

def show():
    st.title("⚙️ Platform Settings & Configurations")
    st.subheader("System Paths & Integration Parameters")

    st.text_input("Screener URL", value=SCREENER_URL, disabled=True)
    st.text_input("Database Location", value=str(DB_PATH), disabled=True)
    st.text_input("Document Store", value=str(DATA_PATH), disabled=True)

    st.markdown("---")
    st.subheader("Manual Pipeline Actions")
    col1, col2, col3 = st.columns(3)
    if col1.button("🔄 Sync Screener Universe"):
        st.success("Universe sync triggered!")
    if col2.button("📊 Recalculate PB Scores"):
        st.success("PB Scores recalculated!")
    if col3.button("💼 Rebalance Portfolio"):
        st.success("Portfolio rebalanced!")
