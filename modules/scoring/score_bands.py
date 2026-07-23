import yaml
from pathlib import Path

class ScoreBandsConfig:
    def __init__(self, config_path="config/score_bands.yaml"):
        self.config = {}
        p = Path(config_path)
        if p.exists():
            with open(p, 'r') as f:
                self.config = yaml.safe_load(f).get("financial", {})

    def get_bands(self, metric_name: str):
        return self.config.get(metric_name, {}).get("bands", [])
