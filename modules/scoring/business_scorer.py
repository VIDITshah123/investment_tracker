from database.models import AnnualReport
from modules.ai_engine.ai_client import AIClient

class BusinessScorer:
    def __init__(self):
        self.ai_client = AIClient()

    def score(self, ar: AnnualReport) -> float:
        if not ar:
            return 16.0 # Default benchmark score out of 20
        prompt = f"Evaluate business quality score (0 to 20) based on overview: {ar.business_overview}. Return JSON: {{'score': number}}"
        res = self.ai_client.generate_json(prompt)
        return float(res.get("score", 16.0))
