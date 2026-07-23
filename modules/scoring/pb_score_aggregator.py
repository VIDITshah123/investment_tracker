import sys
import logging
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Financial, Score, AnnualReport, Transcript, Alert
from modules.scoring.financial_scorer import FinancialScorer
from modules.scoring.business_scorer import BusinessScorer
from modules.scoring.management_scorer import ManagementScorer
from modules.scoring.future_scorer import FutureScorer

logger = logging.getLogger(__name__)

def calculate_all_scores():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    fin_scorer = FinancialScorer()
    bus_scorer = BusinessScorer()
    mgt_scorer = ManagementScorer()
    fut_scorer = FutureScorer()

    companies = session.query(Company).filter(Company.is_active == True).all()
    logger.info(f"Calculating PB Equity Scores for {len(companies)} companies...")

    for comp in companies:
        latest_fin = session.query(Financial).filter_by(company_id=comp.id).order_by(Financial.scraped_at.desc()).first()
        latest_ar = session.query(AnnualReport).filter_by(company_id=comp.id).order_by(AnnualReport.processed_at.desc()).first()
        latest_tr = session.query(Transcript).filter_by(company_id=comp.id).order_by(Transcript.processed_at.desc()).first()

        f_score = fin_scorer.score(latest_fin)
        b_score = bus_scorer.score(latest_ar)
        m_score = mgt_scorer.score(latest_tr)
        u_score = fut_scorer.score(latest_ar, latest_tr)

        pb_score = round(f_score + b_score + m_score + u_score, 1)

        prev_score_obj = session.query(Score).filter_by(company_id=comp.id).order_by(Score.score_date.desc()).first()
        if prev_score_obj and abs(prev_score_obj.pb_score - pb_score) >= 3.0:
            alert = Alert(
                company_id=comp.id,
                alert_type="score_change",
                message=f"PB Score for {comp.company_name} changed: {prev_score_obj.pb_score} -> {pb_score}"
            )
            session.add(alert)

        score_record = Score(
            company_id=comp.id,
            score_date=datetime.utcnow().date(),
            financial_score=f_score,
            business_score=b_score,
            management_score=m_score,
            future_score=u_score,
            pb_score=pb_score
        )
        session.add(score_record)

    session.commit()
    logger.info("PB Equity Score calculation completed.")

if __name__ == "__main__":
    calculate_all_scores()
