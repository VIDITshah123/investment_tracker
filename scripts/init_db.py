import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import SQLALCHEMY_DATABASE_URI, DB_PATH
from database.models import Base

def init_db():
    print(f"Initializing database at: {DB_PATH}")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    # Create tables
    Base.metadata.create_all(engine)
    
    # Enable WAL mode for SQLite performance
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.commit()
        
    print("Database initialized successfully with WAL mode enabled.")

if __name__ == "__main__":
    init_db()
