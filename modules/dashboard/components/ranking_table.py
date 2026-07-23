import streamlit as st
import pandas as pd

def render_ranking_table(df: pd.DataFrame):
    st.dataframe(
        df,
        column_config={
            "PB Score": st.column_config.NumberColumn("PB Score", format="%.1f ⭐"),
            "Financial": st.column_config.NumberColumn("Financial (/40)", format="%.1f"),
            "Business": st.column_config.NumberColumn("Business (/20)", format="%.1f"),
            "Management": st.column_config.NumberColumn("Management (/20)", format="%.1f"),
            "Future": st.column_config.NumberColumn("Future (/20)", format="%.1f"),
        },
        use_container_width=True,
        hide_index=True
    )
