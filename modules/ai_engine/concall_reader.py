import logging
from modules.ai_engine.ai_client import AIClient
from modules.ai_engine.pdf_extractor import PDFExtractor

logger = logging.getLogger(__name__)

class ConcallReader:
    def __init__(self):
        self.ai_client = AIClient()

    def analyze(self, pdf_path: str) -> dict:
        raw_text = PDFExtractor.extract_text(pdf_path, max_pages=30)
        prompt = f"""
Analyze the following Earnings Call (Concall) Transcript and extract insights in JSON format:

Text Snippet:
{raw_text[:4000]}

Extract JSON with keys:
- revenue_drivers
- margin_commentary
- working_capital
- debt_guidance
- management_guidance
- capacity_expansion
- risks (array)
- qa_highlights
- future_outlook
- summary_2min
- management_confidence_score (number 0 to 10)
"""
        return self.ai_client.generate_json(prompt)
