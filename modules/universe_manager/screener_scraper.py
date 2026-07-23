import sys
import re
import logging
import requests
from bs4 import BeautifulSoup
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import SCREENER_EMAIL, SCREENER_PASSWORD, SCREENER_URL

logger = logging.getLogger(__name__)

class ScreenerScraper:
    def __init__(self, url=SCREENER_URL, email=SCREENER_EMAIL, password=SCREENER_PASSWORD):
        self.url = url
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def login(self):
        if not self.email or self.email == "your_screener_email_here":
            logger.info("No Screener credentials provided. Proceeding without authentication.")
            return False

        logger.info(f"Authenticating with Screener.in as {self.email}...")
        login_url = "https://www.screener.in/login/"
        try:
            get_resp = self.session.get(login_url, timeout=15)
            soup = BeautifulSoup(get_resp.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
            
            if not csrf_token:
                logger.warning("CSRF token not found on login page.")
                return False

            payload = {
                "csrfmiddlewaretoken": csrf_token['value'],
                "username": self.email,
                "password": self.password,
                "next": self.url
            }
            headers = {
                "Referer": login_url,
                "Origin": "https://www.screener.in"
            }
            post_resp = self.session.post(login_url, data=payload, headers=headers, timeout=15)
            if post_resp.status_code == 200 or "logout" in post_resp.text.lower():
                logger.info("Successfully authenticated with Screener.in!")
                return True
            else:
                logger.warning("Screener login attempted but response did not confirm session.")
                return False
        except Exception as e:
            logger.error(f"Screener authentication error: {e}")
            return False

    def scrape(self):
        # Attempt login first
        self.login()

        logger.info(f"Scraping Screener universe from {self.url}")
        companies = []
        page = 1

        while True:
            # Append limit=100 and page number to URL query params
            sep = "&" if "?" in self.url else "?"
            page_url = f"{self.url}{sep}limit=100&page={page}"
            logger.info(f"Fetching page {page}: {page_url}")

            try:
                resp = self.session.get(page_url, timeout=15)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                table = soup.find('table', class_='data-table')
                if not table:
                    if page == 1:
                        logger.warning("Could not find data-table in response HTML.")
                    break

                # Dynamic column index mapping from table header (thead)
                col_map = {}
                thead = table.find('thead')
                headers = thead.find_all('th') if thead else table.find_all('th')
                for idx, th in enumerate(headers):
                    txt = th.text.strip().lower()
                    if idx > 0 and 's.no' in txt:
                        break  # Stop at duplicate bottom header row

                    tooltip = (th.get('data-tooltip') or '').lower()
                    link = th.find('a')
                    aria_label = (link.get('aria-label') or '').lower() if link else ''
                    full_txt = (txt + " " + tooltip + " " + aria_label).lower()

                    if 'name' in full_txt and 'name' not in col_map:
                        col_map['name'] = idx
                    elif 'cmp' in full_txt or 'current price' in full_txt:
                        col_map['cmp'] = idx
                    elif 'p/e' in full_txt or 'price to earning' in full_txt:
                        col_map['pe'] = idx
                    elif 'mar cap' in full_txt or 'market cap' in full_txt:
                        col_map['mcap'] = idx
                    elif 'roce' in full_txt or 'return on capital' in full_txt:
                        col_map['roce'] = idx
                    elif 'cf operations' in full_txt or 'cash from operations' in full_txt:
                        col_map['cf_ops'] = idx
                    elif 'pat ann' in full_txt or 'profit after tax' in full_txt:
                        col_map['pat_ann'] = idx
                    elif 'ebit ann' in full_txt or 'ebit' in full_txt:
                        col_map['ebit_ann'] = idx

                rows = table.find_all('tr')
                page_count = 0
                for row in rows:
                    cols = row.find_all('td')
                    if not cols or len(cols) < 2:
                        continue
                    
                    name_idx = col_map.get('name', 1)
                    if name_idx >= len(cols):
                        name_idx = 1
                    
                    link = cols[name_idx].find('a') if name_idx < len(cols) else None
                    if link:
                        name = link.text.strip()
                        href = link.get('href', '')
                        match = re.search(r'/company/([^/]+)/', href)
                        symbol = match.group(1) if match else name.upper().replace(' ', '')

                        def parse_col_val(key):
                            c_idx = col_map.get(key)
                            if c_idx is not None and c_idx < len(cols):
                                txt = cols[c_idx].text.strip().replace(',', '').replace('Rs.', '').replace('%', '')
                                try:
                                    return float(txt) if txt and txt != '-' else None
                                except ValueError:
                                    return None
                            return None

                        cmp_val = parse_col_val('cmp')
                        pe_val = parse_col_val('pe')
                        mcap_val = parse_col_val('mcap')
                        roce_val = parse_col_val('roce')
                        cf_ops = parse_col_val('cf_ops')
                        pat_ann = parse_col_val('pat_ann')
                        ebit_ann = parse_col_val('ebit_ann')

                        companies.append({
                            "name": name,
                            "symbol": symbol,
                            "screener_url": f"https://www.screener.in{href}",
                            "cmp": cmp_val,
                            "pe": pe_val,
                            "mcap": mcap_val,
                            "roce": roce_val,
                            "cf_ops": cf_ops,
                            "pat_ann": pat_ann,
                            "ebit_ann": ebit_ann
                        })
                        page_count += 1

                if page_count == 0:
                    break

                # Check if there is a next page
                pagination = soup.find('div', class_='pagination')
                next_btn = soup.find('a', string=re.compile(r'Next', re.I)) if pagination else None
                if not next_btn or page_count < 100:
                    break

                page += 1

            except Exception as e:
                logger.error(f"Failed to scrape page {page} of Screener.in: {e}")
                break
        
        logger.info(f"Successfully scraped total {len(companies)} companies across {page} page(s) from Screener.")
        return companies

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = ScreenerScraper()
    data = scraper.scrape()
    print(f"Scraped {len(data)} companies.")
    if data:
        print("Sample company scraped:", data[0])
