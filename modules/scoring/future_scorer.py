from database.models import AnnualReport, Transcript
from modules.ai_engine.ai_client import AIClient

class FutureScorer:
    def __init__(self):
        self.ai_client = AIClient()

    def score(self, ar: AnnualReport, transcript: Transcript) -> float:
        if not ar and not transcript:
            return 17.5 # Default benchmark score out of 20
        prompt = "Evaluate future outlook score (0 to 20) based on expansion and industry demand. Return JSON: {'score': number}"
        res = self.ai_client.generate_json(prompt)
        return float(res.get("score", 17.5))
