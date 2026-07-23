import os
import logging
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFDownloader:
    @staticmethod
    def download(url: str, save_dir: Path, filename: str) -> Path:
        save_dir.mkdir(parents=True, exist_ok=True)
        file_path = save_dir / filename
        
        if file_path.exists():
            logger.info(f"File already exists: {file_path}")
            return file_path

        logger.info(f"Downloading PDF from {url} to {file_path}")
        try:
            resp = requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            resp.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return file_path
        except Exception as e:
            logger.error(f"Download failed for {url}: {e}")
            return None
