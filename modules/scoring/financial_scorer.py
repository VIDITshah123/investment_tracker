from database.models import Financial
from modules.scoring.score_bands import ScoreBandsConfig

class FinancialScorer:
    def __init__(self):
        self.bands_config = ScoreBandsConfig()

    def score(self, financial: Financial) -> float:
        if not financial:
            return 0.0

        total_score = 0.0

        # ROCE (max 8)
        roce = financial.roce or 0.0
        for band in self.bands_config.get_bands("roce"):
            if roce >= band.get("min", 0):
                total_score += band.get("score", 0)
                break

        # CFO / PAT (max 6)
        cfo_pat = financial.cfo_pat_ratio or 0.0
        for band in self.bands_config.get_bands("cfo_pat_ratio"):
            if cfo_pat >= band.get("min", 0):
                total_score += band.get("score", 0)
                break

        # CFO / EBITDA (max 6)
        cfo_ebitda = financial.cfo_ebitda or 0.0
        for band in self.bands_config.get_bands("cfo_ebitda"):
            if cfo_ebitda >= band.get("min", 0):
                total_score += band.get("score", 0)
                break

        # Sales Growth 3Y (max 5)
        sales_g = financial.sales_growth_3y or 18.0 # Default benchmark
        for band in self.bands_config.get_bands("sales_growth_3y"):
            if sales_g >= band.get("min", 0):
                total_score += band.get("score", 0)
                break

        # Profit Growth 3Y (max 5)
        profit_g = financial.profit_growth_3y or 18.0 # Default benchmark
        for band in self.bands_config.get_bands("profit_growth_3y"):
            if profit_g >= band.get("min", 0):
                total_score += band.get("score", 0)
                break

        # Debt to Equity (max 5)
        de = financial.debt_equity or 0.2
        for band in self.bands_config.get_bands("debt_equity"):
            if de <= band.get("max", 999):
                total_score += band.get("score", 0)
                break

        # Interest Coverage (max 3)
        ic = financial.interest_coverage or 10.0
        for band in self.bands_config.get_bands("interest_coverage"):
            if ic >= band.get("min", 0):
                total_score += band.get("score", 0)
                break

        # Promoter Holding (max 1)
        ph = financial.promoter_holding or 55.0
        for band in self.bands_config.get_bands("promoter_holding"):
            if ph >= band.get("min", 0):
                total_score += band.get("score", 0)
                break

        # Dividend Yield (max 1)
        dy = financial.dividend_yield or 0.5
        for band in self.bands_config.get_bands("dividend_yield"):
            if dy >= band.get("min", 0):
                total_score += band.get("score", 0)
                break

        return min(round(total_score, 1), 40.0)
