# from sqlalchemy import Column, Integer, String, Text, create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# from ..config import settings

# Base = declarative_base()
# engine = create_engine(settings.DATABASE_URL, future=True)
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# class StoredBrand(Base):
#     __tablename__ = 'brands'

#     id = Column(Integer, primary_key=True, index=True)
#     website_url = Column(String(500), unique=True, nullable=False)
#     brand_name = Column(String(255))
#     json_blob = Column(Text)  # store full JSON snapshot as text

# def init_db():
#     Base.metadata.create_all(bind=engine)




from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BrandInsight(Base):
    __tablename__ = "brand_insights"
    id = Column(Integer, primary_key=True, index=True)
    website_url = Column(String, unique=True, index=True)
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)