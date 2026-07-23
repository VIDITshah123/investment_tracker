import time
import logging
import schedule
from modules.universe_manager.universe_sync import sync_universe
from modules.scoring.pb_score_aggregator import calculate_all_scores
from modules.ranking.ranking_engine import update_rankings
from modules.ranking.portfolio_engine import generate_portfolio_recommendations

logger = logging.getLogger(__name__)

def daily_pipeline():
    logger.info("Running Daily Pipeline...")
    sync_universe()

def quarterly_pipeline():
    logger.info("Running Quarterly Pipeline...")
    calculate_all_scores()
    update_rankings()
    generate_portfolio_recommendations()

def start_scheduler():
    logger.info("Starting Automation Scheduler...")
    schedule.every().day.at("07:00").do(daily_pipeline)
    schedule.every().monday.at("08:00").do(quarterly_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()
