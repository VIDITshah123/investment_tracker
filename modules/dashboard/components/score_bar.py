import streamlit as st

def render_score_bar(label: str, score: float, max_score: float):
    ratio = score / max_score if max_score else 0
    color = "green" if ratio >= 0.8 else "orange" if ratio >= 0.6 else "red"
    st.write(f"**{label}:** {score} / {max_score}")
    st.progress(min(max(ratio, 0.0), 1.0))
