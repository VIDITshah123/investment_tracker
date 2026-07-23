import hashlib
from pathlib import Path

class Deduplicator:
    @staticmethod
    def get_file_hash(file_path: Path) -> str:
        if not file_path.exists():
            return ""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
