import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, Portfolio, Watchlist

logger = logging.getLogger(__name__)

def generate_portfolio_recommendations():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Portfolio).delete()
    session.query(Watchlist).delete()

    companies = session.query(Company).filter(Company.is_active == True).all()
    scored_list = []
    for c in companies:
        s = session.query(Score).filter_by(company_id=c.id).order_by(Score.created_at.desc()).first()
        if s:
            scored_list.append((c, s))

    scored_list.sort(key=lambda x: x[1].pb_score, reverse=True)

    for idx, (c, s) in enumerate(scored_list):
        if idx < 10:
            p = Portfolio(
                company_id=c.id,
                portfolio_type="Top 10",
                suggested_weight=10.0,
                rationale=f"Rank #{idx+1} with outstanding PB Score of {s.pb_score}"
            )
            session.add(p)
        elif idx < 20:
            p = Portfolio(
                company_id=c.id,
                portfolio_type="Top 20",
                suggested_weight=5.0,
                rationale=f"Rank #{idx+1} with strong PB Score of {s.pb_score}"
            )
            session.add(p)
        else:
            w = Watchlist(
                company_id=c.id,
                target_pb_score=80.0,
                notes="Watch for score improvement"
            )
            session.add(w)

    session.commit()
    logger.info("Portfolio and Watchlist generated.")

if __name__ == "__main__":
    generate_portfolio_recommendations()
