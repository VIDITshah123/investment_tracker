import json
import logging
from modules.ai_engine.ai_client import AIClient
from modules.ai_engine.pdf_extractor import PDFExtractor

logger = logging.getLogger(__name__)

class AnnualReportReader:
    def __init__(self):
        self.ai_client = AIClient()

    def analyze(self, pdf_path: str) -> dict:
        raw_text = PDFExtractor.extract_text(pdf_path, max_pages=30)
        prompt = f"""
Analyze the following Annual Report text and extract structured business insights in JSON format:

Text Snippet:
{raw_text[:4000]}

Extract JSON with keys:
- business_overview
- products_services
- customer_profile
- geography
- key_risks (array)
- capex_plans
- management_quality
- competitive_position
- moat_assessment ("High", "Medium", or "Low")
- growth_drivers (array)
- summary_2min
"""
        return self.ai_client.generate_json(prompt)
