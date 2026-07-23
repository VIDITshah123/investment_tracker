import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company
from modules.company_master.ir_discovery import IRDiscovery
from modules.company_master.bse_lookup import BSELookup

logger = logging.getLogger(__name__)

def build_company_master():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    discovery = IRDiscovery()
    companies = session.query(Company).filter(Company.is_active == True).all()

    logger.info(f"Building Company Master for {len(companies)} active companies...")
    for comp in companies:
        if not comp.bse_code:
            comp.bse_code = BSELookup.get_bse_code(comp.nse_symbol)
        
        if not comp.official_url or not comp.ir_url:
            res = discovery.discover_urls(comp.company_name, comp.nse_symbol)
            comp.official_url = comp.official_url or res["official_url"]
            comp.ir_url = comp.ir_url or res["ir_url"]

    session.commit()
    logger.info("Company Master build complete.")

if __name__ == "__main__":
    build_company_master()
