import logging

logger = logging.getLogger(__name__)

# Known BSE Code Mapping for initial live universe
BSE_MAP = {
    "MCX": "533122",
    "HBLENGINE": "540115",
    "HINDCOPPER": "513599",
    "FORCEMOT": "500033",
    "SIKA": "524642",
    "ALGOQUANT": "504369",
    "SMLMAH": "520121",
    "TRENT": "500251",
    "ALLDIGI": "532927",
    "DANLAW": "532329",
    "CARERATING": "532540",
    "PRICOLLTD": "540293",
    "RAILTEL": "543265",
    "KOVAI": "523323",
    "SEAMECLTD": "526761",
    "GULPOLY": "524226",
    "DEEPINDS": "543241"
}

class BSELookup:
    @staticmethod
    def get_bse_code(nse_symbol: str) -> str:
        return BSE_MAP.get(nse_symbol.upper(), "500000")
