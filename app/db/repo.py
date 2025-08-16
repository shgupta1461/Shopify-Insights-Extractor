# import json
# from contextlib import contextmanager
# from .models import SessionLocal, StoredBrand

# @contextmanager
# def session_scope():
#     """Provide a transactional scope around a series of operations."""
#     db = SessionLocal()
#     try:
#         yield db
#         db.commit()
#     except Exception:
#         db.rollback()
#         raise
#     finally:
#         db.close()

# def save_brand(website_url: str, brand_name: str, payload: dict):
#     """Insert or update a stored brand snapshot."""
#     with session_scope() as db:
#         rec = db.query(StoredBrand).filter(StoredBrand.website_url == website_url).one_or_none()
#         if rec is None:
#             rec = StoredBrand(website_url=website_url)
#         rec.brand_name = brand_name
#         rec.json_blob = json.dumps(payload)
#         db.add(rec)

# def get_brand(website_url: str):
#     """Retrieve a stored brand snapshot by website URL."""
#     with session_scope() as db:
#         rec = db.query(StoredBrand).filter(StoredBrand.website_url == website_url).one_or_none()
#         if not rec:
#             return None
#         return {
#             "website_url": rec.website_url,
#             "brand_name": rec.brand_name,
#             "payload": json.loads(rec.json_blob),
#         }



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, BrandInsight

DATABASE_URL = "sqlite:///./shopify_insights.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# def save_brand_insight(website_url, data):
#     session = SessionLocal()
#     try:
#         insight = BrandInsight(website_url=website_url, data=data)
#         session.add(insight)
#         session.commit()
#         session.refresh(insight)
#         return insight
#     finally:
#         session.close()

def save_brand_insight(website_url, data):
    session = SessionLocal()
    try:
        insight = session.query(BrandInsight).filter_by(website_url=website_url).first()
        if insight:
            insight.data = data
        else:
            insight = BrandInsight(website_url=website_url, data=data)
            session.add(insight)
        session.commit()
        session.refresh(insight)
        return insight
    finally:
        session.close()