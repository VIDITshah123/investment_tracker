from database.models import Transcript
from modules.ai_engine.ai_client import AIClient

class ManagementScorer:
    def __init__(self):
        self.ai_client = AIClient()

    def score(self, transcript: Transcript) -> float:
        if not transcript:
            return 17.0 # Default benchmark score out of 20
        prompt = f"Evaluate management quality & guidance honesty score (0 to 20) based on transcript summary: {transcript.summary_2min}. Return JSON: {{'score': number}}"
        res = self.ai_client.generate_json(prompt)
        return float(res.get("score", 17.0))
