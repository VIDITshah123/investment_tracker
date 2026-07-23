from modules.ai_engine.ai_client import AIClient

class Summarizer:
    def __init__(self):
        self.ai_client = AIClient()

    def generate_2min_summary(self, text: str) -> str:
        prompt = f"Provide a concise 2-minute executive summary for this text:\n\n{text[:3000]}"
        res = self.ai_client.generate_json(prompt)
        return res.get("summary_2min") or res.get("summary") or "Executive summary unavailable."
