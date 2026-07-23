import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import SQLALCHEMY_DATABASE_URI, DATA_PATH
from database.models import Company, AnnualReport, Transcript
from modules.document_collector.ir_crawler import IRCrawler
from modules.document_collector.pdf_downloader import PDFDownloader
from modules.document_collector.document_classifier import DocumentClassifier

logger = logging.getLogger(__name__)

def collect_documents(symbol: str = None):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    crawler = IRCrawler()
    downloader = PDFDownloader()

    query = session.query(Company).filter(Company.is_active == True)
    if symbol:
        query = query.filter(Company.nse_symbol == symbol)
    companies = query.all()

    logger.info(f"Starting Document Collector for {len(companies)} companies...")
    for comp in companies:
        if not comp.ir_url:
            continue
        docs = crawler.crawl(comp.nse_symbol, comp.ir_url)
        save_dir = DATA_PATH / comp.nse_symbol / "FY26"
        
        for doc in docs[:3]: # Limit to top 3 documents per company for initial run
            doc_type = DocumentClassifier.classify(doc["title"])
            clean_filename = f"{doc_type}_{Path(doc['url']).name}"
            downloaded_path = downloader.download(doc["url"], save_dir, clean_filename)
            
            if downloaded_path:
                if doc_type == 'AnnualReport':
                    existing = session.query(AnnualReport).filter_by(company_id=comp.id, fiscal_year="FY26").first()
                    if not existing:
                        ar = AnnualReport(company_id=comp.id, fiscal_year="FY26", document_path=str(downloaded_path))
                        session.add(ar)
                elif doc_type == 'ConcallTranscript':
                    existing = session.query(Transcript).filter_by(company_id=comp.id, fiscal_year="FY26", quarter="Q1").first()
                    if not existing:
                        tr = Transcript(company_id=comp.id, fiscal_year="FY26", quarter="Q1", document_path=str(downloaded_path))
                        session.add(tr)

    session.commit()
    logger.info("Document Collection finished.")

if __name__ == "__main__":
    collect_documents()
