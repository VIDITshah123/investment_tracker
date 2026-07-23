import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

import streamlit as st
from modules.ai_chat.query_router import QueryRouter

def show():
    st.title("🤖 AI Research Assistant")
    st.caption("Ask natural language questions about your companies, scores, concalls, or rankings.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello Pratik! I am your PB Equity Research Assistant. Ask me anything about your stock universe."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("e.g. Which company has the strongest management score?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        router = QueryRouter()
        answer = router.answer_query(prompt)

        with st.chat_message("assistant"):
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
