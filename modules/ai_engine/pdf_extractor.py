import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFExtractor:
    @staticmethod
    def extract_text(file_path: str, max_pages: int = 50) -> str:
        p = Path(file_path)
        if not p.exists():
            logger.warning(f"File not found: {file_path}")
            return ""

        text = ""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            for page in doc[:max_pages]:
                text += page.get_text() + "\n"
            logger.info(f"Extracted {len(text)} chars from {file_path}")
        except Exception as e:
            logger.warning(f"PyMuPDF failed for {file_path}: {e}")
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages[:max_pages]:
                        text += page.extract_text() or ""
            except Exception as e2:
                logger.error(f"pdfplumber also failed: {e2}")

        return text
