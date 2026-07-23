import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Score, SectorRank

logger = logging.getLogger(__name__)

def update_rankings():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Get latest score per active company
    companies = session.query(Company).filter(Company.is_active == True).all()
    comp_scores = []
    for c in companies:
        s = session.query(Score).filter_by(company_id=c.id).order_by(Score.created_at.desc()).first()
        if s:
            comp_scores.append((c, s))

    # Overall Rank (descending by pb_score)
    comp_scores.sort(key=lambda x: x[1].pb_score, reverse=True)
    for idx, (c, s) in enumerate(comp_scores, start=1):
        s.overall_rank = idx

    # Sector Rank
    sectors = set(c.sector for c, s in comp_scores if c.sector)
    for sector in sectors:
        sec_comps = [(c, s) for c, s in comp_scores if c.sector == sector]
        sec_comps.sort(key=lambda x: x[1].pb_score, reverse=True)
        for idx, (c, s) in enumerate(sec_comps, start=1):
            s.sector_rank = idx
        
        # SectorRank table aggregate
        avg_sc = sum(s.pb_score for c, s in sec_comps) / len(sec_comps)
        sr_entry = session.query(SectorRank).filter_by(sector_name=sector).first()
        if not sr_entry:
            sr_entry = SectorRank(sector_name=sector)
            session.add(sr_entry)
        sr_entry.avg_score = round(avg_sc, 1)
        sr_entry.company_count = len(sec_comps)
        sr_entry.top_company_id = sec_comps[0][0].id

    session.commit()
    logger.info(f"Updated rankings for {len(comp_scores)} companies.")

if __name__ == "__main__":
    update_rankings()
