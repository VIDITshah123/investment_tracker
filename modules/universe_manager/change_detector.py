import logging
from sqlalchemy.orm import Session
from database.models import Company

logger = logging.getLogger(__name__)

class ChangeDetector:
    def __init__(self, db_session: Session):
        self.session = db_session

    def detect_changes(self, scraped_companies: list):
        active_db_companies = self.session.query(Company).filter(Company.is_active == True).all()
        active_db_symbols = {c.nse_symbol: c for c in active_db_companies}
        scraped_symbols = {c['symbol']: c for c in scraped_companies}

        new_companies = []
        for symbol, data in scraped_symbols.items():
            if symbol not in active_db_symbols:
                new_companies.append(data)

        removed_companies = []
        for symbol, company_obj in active_db_symbols.items():
            if symbol not in scraped_symbols:
                removed_companies.append(company_obj)

        logger.info(f"Detected {len(new_companies)} new companies, {len(removed_companies)} removed companies.")
        return new_companies, removed_companies
