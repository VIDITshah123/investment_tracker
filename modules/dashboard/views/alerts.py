import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Alert

def show():
    st.title("🔔 Alerts & System Notifications")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    alerts = session.query(Alert).order_by(Alert.created_at.desc()).all()
    if alerts:
        for a in alerts:
            st.info(f"**[{a.created_at.strftime('%Y-%m-%d %H:%M')}] [{a.alert_type.upper()}]** {a.message}")
    else:
        st.info("No system alerts logged.")
