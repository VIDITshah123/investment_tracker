from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, Financial, AnnualReport, Transcript

class ContextBuilder:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def get_company_context(self, symbol: str):
        session = self.Session()
        comp = session.query(Company).filter_by(nse_symbol=symbol).first()
        if not comp:
            return f"No data found for symbol {symbol}."
        
        score = session.query(Score).filter_by(company_id=comp.id).order_by(Score.created_at.desc()).first()
        fin = session.query(Financial).filter_by(company_id=comp.id).order_by(Financial.scraped_at.desc()).first()
        
        return f"{comp.company_name} ({comp.nse_symbol}) has a PB Score of {score.pb_score if score else 'N/A'}/100. Sector: {comp.sector}. ROCE: {fin.roce if fin else 'N/A'}%."
