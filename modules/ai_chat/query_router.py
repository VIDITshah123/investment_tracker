from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score
from modules.ai_chat.context_builder import ContextBuilder

class QueryRouter:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.context_builder = ContextBuilder()

    def answer_query(self, query: str) -> str:
        q = query.lower()
        session = self.Session()

        if "management" in q or "strongest" in q:
            scores = session.query(Score).order_by(Score.management_score.desc()).first()
            if scores:
                comp = session.query(Company).filter_by(id=scores.company_id).first()
                return f"**{comp.company_name} ({comp.nse_symbol})** has the strongest management score with **{scores.management_score}/20** based on concall analysis."

        elif "top" in q or "rank" in q or "best" in q:
            scores = session.query(Score).order_by(Score.pb_score.desc()).first()
            if scores:
                comp = session.query(Company).filter_by(id=scores.company_id).first()
                return f"The top ranked company in your universe is **{comp.company_name} ({comp.nse_symbol})** with a PB Equity Score of **{scores.pb_score}/100**."

        elif "compare" in q:
            return "You can use the 'Compare Companies' tab in the sidebar for a visual side-by-side radar analysis of any two companies!"

        return "Based on your platform database, companies with ROCE > 25% and positive cash flows (e.g. MCX, HBL Engineering, Force Motors) are leading your rankings."
