import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import SQLALCHEMY_DATABASE_URI
from database.models import Company, Financial, Score

COMPANIES_DATA = [
    {"name": "Multi Comm. Exc.", "symbol": "MCX", "sector": "Financial Services", "industry": "Exchange", "cmp": 2752.60, "pe": 52.70, "mcap": 70177.79, "roce": 71.37, "cf_ops": 3034.72, "pat_ann": 1331.55, "ebit_ann": 1690.69},
    {"name": "HBL Engineering", "symbol": "HBLENGINE", "sector": "Capital Goods", "industry": "Batteries/Electrical", "cmp": 704.95, "pe": 23.27, "mcap": 19498.44, "roce": 58.45, "cf_ops": 738.44, "pat_ann": 837.90, "ebit_ann": 1121.35},
    {"name": "Hindustan Copper", "symbol": "HINDCOPPER", "sector": "Metals & Mining", "industry": "Copper", "cmp": 491.80, "pe": 48.05, "mcap": 47558.24, "roce": 42.40, "cf_ops": 1473.57, "pat_ann": 989.82, "ebit_ann": 1333.39},
    {"name": "Force Motors", "symbol": "FORCEMOT", "sector": "Automobile", "industry": "Commercial Vehicles", "cmp": 17410.00, "pe": 21.71, "mcap": 22933.68, "roce": 36.08, "cf_ops": 1297.09, "pat_ann": 1056.51, "ebit_ann": 1307.73},
    {"name": "Sika Interplant", "symbol": "SIKA", "sector": "Capital Goods", "industry": "Aerospace & Defense", "cmp": 1133.20, "pe": 68.39, "mcap": 2401.97, "roce": 34.56, "cf_ops": 46.91, "pat_ann": 35.12, "ebit_ann": 48.29},
    {"name": "Algoquant Fin", "symbol": "ALGOQUANT", "sector": "Financial Services", "industry": "Capital Market Services", "cmp": 65.42, "pe": 56.11, "mcap": 1837.00, "roce": 31.43, "cf_ops": 60.13, "pat_ann": 32.74, "ebit_ann": 47.89},
    {"name": "SML Mahindra", "symbol": "SMLMAH", "sector": "Automobile", "industry": "Commercial Vehicles", "cmp": 3899.30, "pe": 36.09, "mcap": 5645.35, "roce": 30.90, "cf_ops": 156.19, "pat_ann": 159.65, "ebit_ann": 234.56},
    {"name": "Trent", "symbol": "TRENT", "sector": "Consumer Services", "industry": "Retail", "cmp": 2874.80, "pe": 88.79, "mcap": 153280.35, "roce": 28.34, "cf_ops": 2667.62, "pat_ann": 1726.25, "ebit_ann": 2478.11},
    {"name": "Alldigi Tech", "symbol": "ALLDIGI", "sector": "Information Technology", "industry": "IT Enabled Services", "cmp": 836.05, "pe": 16.01, "mcap": 1286.35, "roce": 27.89, "cf_ops": 144.09, "pat_ann": 80.36, "ebit_ann": 103.79},
    {"name": "Danlaw Tech.", "symbol": "DANLAW", "sector": "Information Technology", "industry": "Software", "cmp": 1016.70, "pe": 21.54, "mcap": 495.21, "roce": 27.22, "cf_ops": 20.62, "pat_ann": 22.99, "ebit_ann": 32.89},
    {"name": "CARE Ratings", "symbol": "CARERATING", "sector": "Financial Services", "industry": "Financial Rating", "cmp": 1729.20, "pe": 30.40, "mcap": 5203.75, "roce": 26.30, "cf_ops": 147.57, "pat_ann": 171.18, "ebit_ann": 237.85},
    {"name": "Pricol Ltd", "symbol": "PRICOLLTD", "sector": "Automobile", "industry": "Auto Ancillaries", "cmp": 626.10, "pe": 30.79, "mcap": 7636.05, "roce": 24.50, "cf_ops": 281.26, "pat_ann": 247.99, "ebit_ann": 358.73},
    {"name": "Railtel Corpn.", "symbol": "RAILTEL", "sector": "Telecommunication", "industry": "Telecom Services", "cmp": 287.55, "pe": 25.36, "mcap": 9225.40, "roce": 22.78, "cf_ops": 316.45, "pat_ann": 363.79, "ebit_ann": 497.72},
    {"name": "Kovai Medical", "symbol": "KOVAI", "sector": "Healthcare", "industry": "Hospital", "cmp": 5750.50, "pe": 25.74, "mcap": 6291.71, "roce": 22.19, "cf_ops": 361.83, "pat_ann": 244.46, "ebit_ann": 357.72},
    {"name": "SEAMEC Ltd", "symbol": "SEAMECLTD", "sector": "Energy", "industry": "Offshore Logistics", "cmp": 1402.10, "pe": 14.16, "mcap": 3559.90, "roce": 20.04, "cf_ops": 321.30, "pat_ann": 251.39, "ebit_ann": 290.05},
    {"name": "Gulshan Polyols", "symbol": "GULPOLY", "sector": "Chemicals", "industry": "Specialty Chemicals", "cmp": 186.57, "pe": 10.83, "mcap": 1162.28, "roce": 18.31, "cf_ops": 207.45, "pat_ann": 107.32, "ebit_ann": 186.45},
    {"name": "Deep Industries", "symbol": "DEEPINDS", "sector": "Energy", "industry": "Oil & Gas Services", "cmp": 459.50, "pe": 7.92, "mcap": 2931.43, "roce": 16.48, "cf_ops": 270.09, "pat_ann": 370.13, "ebit_ann": 365.59}
]

def seed():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Seeding initial live universe into database...")
    for item in COMPANIES_DATA:
        company = session.query(Company).filter_by(nse_symbol=item["symbol"]).first()
        if not company:
            company = Company(
                nse_symbol=item["symbol"],
                company_name=item["name"],
                sector=item["sector"],
                industry=item["industry"],
                screener_url=f"https://www.screener.in/company/{item['symbol']}/",
                is_active=True
            )
            session.add(company)
            session.flush()

        # Add initial financial snapshot
        fin = Financial(
            company_id=company.id,
            cmp=item["cmp"],
            pe_ratio=item["pe"],
            market_cap=item["mcap"],
            roce=item["roce"],
            cf_operations=item["cf_ops"],
            pat_ann=item["pat_ann"],
            ebit_ann=item["ebit_ann"],
            cfo_pat_ratio=round(item["cf_ops"] / item["pat_ann"], 2) if item["pat_ann"] else None,
            cfo_ebitda=round(item["cf_ops"] / item["ebit_ann"], 2) if item["ebit_ann"] else None,
            source="screener_live_seed"
        )
        session.add(fin)

    session.commit()
    print(f"Successfully seeded {len(COMPANIES_DATA)} live companies.")

if __name__ == "__main__":
    seed()
