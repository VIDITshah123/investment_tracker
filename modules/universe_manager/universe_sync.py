import sys
import logging
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Financial, Log, Alert
from modules.universe_manager.screener_scraper import ScreenerScraper
from modules.universe_manager.change_detector import ChangeDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sync_universe():
    start_time = datetime.utcnow()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    logger.info("Starting Universe Synchronization...")
    scraper = ScreenerScraper()
    scraped_data = scraper.scrape()

    if not scraped_data:
        logger.warning("No data retrieved from Screener. Aborting sync.")
        log = Log(job_name="universe_sync", status="failure", message="No data retrieved from Screener", duration_s=(datetime.utcnow()-start_time).total_seconds())
        session.add(log)
        session.commit()
        return

    detector = ChangeDetector(session)
    new_cos, removed_cos = detector.detect_changes(scraped_data)

    # Add new companies
    for item in new_cos:
        comp = Company(
            nse_symbol=item["symbol"],
            company_name=item["name"],
            screener_url=item["screener_url"],
            is_active=True,
            added_date=datetime.utcnow().date()
        )
        session.add(comp)
        session.flush()

        alert = Alert(
            company_id=comp.id,
            alert_type="new_company",
            message=f"New company entered Screener universe: {comp.company_name} ({comp.nse_symbol})"
        )
        session.add(alert)
        logger.info(f"Added new company: {comp.company_name}")

    # Mark removed companies as inactive
    for comp in removed_cos:
        comp.is_active = False
        comp.removed_date = datetime.utcnow().date()
        alert = Alert(
            company_id=comp.id,
            alert_type="removed_company",
            message=f"Company removed from Screener universe: {comp.company_name} ({comp.nse_symbol})"
        )
        session.add(alert)
        logger.info(f"Marked company inactive: {comp.company_name}")

    # Update latest financial snapshots for scraped companies
    for item in scraped_data:
        comp = session.query(Company).filter_by(nse_symbol=item["symbol"]).first()
        if comp:
            fin = Financial(
                company_id=comp.id,
                cmp=item.get("cmp"),
                pe_ratio=item.get("pe"),
                market_cap=item.get("mcap"),
                roce=item.get("roce"),
                cf_operations=item.get("cf_ops"),
                pat_ann=item.get("pat_ann"),
                ebit_ann=item.get("ebit_ann"),
                cfo_pat_ratio=round(item["cf_ops"] / item["pat_ann"], 2) if item.get("cf_ops") and item.get("pat_ann") else None,
                cfo_ebitda=round(item["cf_ops"] / item["ebit_ann"], 2) if item.get("cf_ops") and item.get("ebit_ann") else None,
                source="screener_sync"
            )
            session.add(fin)

    duration = (datetime.utcnow() - start_time).total_seconds()
    log = Log(job_name="universe_sync", status="success", message=f"Synced {len(scraped_data)} companies. Added {len(new_cos)}, removed {len(removed_cos)}.", duration_s=duration)
    session.add(log)

    session.commit()
    logger.info(f"Universe Sync completed in {duration:.2f} seconds.")

if __name__ == "__main__":
    sync_universe()
