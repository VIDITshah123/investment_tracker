import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean, Date, DateTime, Text, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nse_symbol = Column(String(50), unique=True, nullable=False)
    bse_code = Column(String(50), nullable=True)
    company_name = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    official_url = Column(Text, nullable=True)
    ir_url = Column(Text, nullable=True)
    screener_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    added_date = Column(Date, default=datetime.utcnow().date)
    removed_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    financials = relationship("Financial", back_populates="company", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="company", cascade="all, delete-orphan")
    transcripts = relationship("Transcript", back_populates="company", cascade="all, delete-orphan")
    annual_reports = relationship("AnnualReport", back_populates="company", cascade="all, delete-orphan")
    management_notes = relationship("ManagementNote", back_populates="company", cascade="all, delete-orphan")

class Financial(Base):
    __tablename__ = 'financials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    fiscal_year = Column(String(20), nullable=True)
    quarter = Column(String(20), nullable=True)
    cmp = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    dividend_yield = Column(Float, nullable=True)
    np_qtr = Column(Float, nullable=True)
    qtr_profit_var = Column(Float, nullable=True)
    sales_qtr = Column(Float, nullable=True)
    qtr_sales_var = Column(Float, nullable=True)
    roce = Column(Float, nullable=True)
    roe = Column(Float, nullable=True)
    cf_operations = Column(Float, nullable=True)
    pat_ann = Column(Float, nullable=True)
    ebit_ann = Column(Float, nullable=True)
    cfo_pat_ratio = Column(Float, nullable=True)
    cfo_ebitda = Column(Float, nullable=True)
    sales_growth_3y = Column(Float, nullable=True)
    profit_growth_3y = Column(Float, nullable=True)
    debt_equity = Column(Float, nullable=True)
    interest_coverage = Column(Float, nullable=True)
    promoter_holding = Column(Float, nullable=True)
    peg_ratio = Column(Float, nullable=True)
    source = Column(String(50), default="screener")
    scraped_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="financials")

class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    score_date = Column(Date, default=datetime.utcnow().date)
    financial_score = Column(Float, default=0.0)
    business_score = Column(Float, default=0.0)
    management_score = Column(Float, default=0.0)
    future_score = Column(Float, default=0.0)
    pb_score = Column(Float, default=0.0)
    overall_rank = Column(Integer, nullable=True)
    sector_rank = Column(Integer, nullable=True)
    industry_rank = Column(Integer, nullable=True)
    financial_rank = Column(Integer, nullable=True)
    business_rank = Column(Integer, nullable=True)
    management_rank = Column(Integer, nullable=True)
    score_version = Column(String(20), default="v1.0")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="scores")

class Transcript(Base):
    __tablename__ = 'transcripts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    fiscal_year = Column(String(20), nullable=True)
    quarter = Column(String(20), nullable=True)
    document_path = Column(Text, nullable=True)
    revenue_drivers = Column(Text, nullable=True)
    margin_commentary = Column(Text, nullable=True)
    working_capital = Column(Text, nullable=True)
    debt_guidance = Column(Text, nullable=True)
    management_guidance = Column(Text, nullable=True)
    capacity_expansion = Column(Text, nullable=True)
    risks = Column(Text, nullable=True)
    qa_highlights = Column(Text, nullable=True)
    future_outlook = Column(Text, nullable=True)
    summary_2min = Column(Text, nullable=True)
    management_confidence_score = Column(Float, nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="transcripts")

class AnnualReport(Base):
    __tablename__ = 'annual_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    fiscal_year = Column(String(20), nullable=True)
    document_path = Column(Text, nullable=True)
    business_overview = Column(Text, nullable=True)
    products_services = Column(Text, nullable=True)
    customer_profile = Column(Text, nullable=True)
    geography = Column(Text, nullable=True)
    key_risks = Column(Text, nullable=True)
    capex_plans = Column(Text, nullable=True)
    management_quality = Column(Text, nullable=True)
    competitive_position = Column(Text, nullable=True)
    moat_assessment = Column(String(50), nullable=True)
    growth_drivers = Column(Text, nullable=True)
    summary_2min = Column(Text, nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="annual_reports")

class ManagementNote(Base):
    __tablename__ = 'management_notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    fiscal_year = Column(String(20), nullable=True)
    quarter = Column(String(20), nullable=True)
    metric = Column(String(100), nullable=True)
    stated_value = Column(String(255), nullable=True)
    direction = Column(String(50), nullable=True)
    quote = Column(Text, nullable=True)
    source_doc_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="management_notes")

class SectorRank(Base):
    __tablename__ = 'sector_ranks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sector_name = Column(String(100), unique=True, nullable=False)
    avg_score = Column(Float, default=0.0)
    company_count = Column(Integer, default=0)
    top_company_id = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    portfolio_type = Column(String(50), nullable=False) # 'Top 10', 'Top 20', 'Avoid'
    suggested_weight = Column(Float, nullable=True)
    rationale = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Watchlist(Base):
    __tablename__ = 'watchlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    target_pb_score = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    message = Column(Text, nullable=True)
    duration_s = Column(Float, nullable=True)
    run_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    alert_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
