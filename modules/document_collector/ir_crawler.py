import logging
import requests
from bs4 import BeautifulSoup
import re
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

class IRCrawler:
    def __init__(self, config_path="config/company_adapters.yaml"):
        self.adapters = {}
        try:
            p = Path(config_path)
            if p.exists():
                with open(p, 'r') as f:
                    self.adapters = yaml.safe_load(f).get("adapters", {})
        except Exception as e:
            logger.warning(f"Failed to load company adapters: {e}")

    def crawl(self, symbol: str, ir_url: str):
        logger.info(f"Crawling IR page for {symbol}: {ir_url}")
        found_docs = []
        
        # Check custom adapter
        adapter = self.adapters.get(symbol.upper())
        if adapter:
            ir_url = adapter.get("ir_url", ir_url)

        try:
            resp = requests.get(ir_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    text = a.text.strip().lower()
                    if href.endswith('.pdf') or 'report' in text or 'transcript' in text or 'concall' in text or 'results' in text:
                        if not href.startswith('http'):
                            href = requests.compat.urljoin(ir_url, href)
                        found_docs.append({
                            "url": href,
                            "title": a.text.strip() or Path(href).name
                        })
        except Exception as e:
            logger.warning(f"Error crawling IR page {ir_url}: {e}")

        logger.info(f"Found {len(found_docs)} potential document links for {symbol}.")
        return found_docs
