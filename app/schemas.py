from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl

class Policy(BaseModel):
    type: str
    url: Optional[str] = None
    content_snippet: Optional[str] = None

class FAQ(BaseModel):
    question: str
    answer: str
    source_url: Optional[str] = None

class Product(BaseModel):
    id: Optional[str] = None
    handle: Optional[str] = None
    title: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    url: Optional[str] = None
    images: Optional[List[str]] = None

class BrandLinks(BaseModel):
    contact_us: Optional[str] = None
    order_tracking: Optional[str] = None
    blog: Optional[str] = None
    about: Optional[str] = None

class SocialHandles(BaseModel):
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    tiktok: Optional[str] = None
    twitter: Optional[str] = None
    youtube: Optional[str] = None
    pinterest: Optional[str] = None
    linkedin: Optional[str] = None

class ContactInfo(BaseModel):
    emails: List[str] = []
    phones: List[str] = []

class BrandContext(BaseModel):
    website_url: HttpUrl
    brand_name: Optional[str] = None
    whole_product_catalog: List[Product] = []
    hero_products: List[Product] = []
    policies: List[Policy] = []
    faqs: List[FAQ] = []
    social_handles: SocialHandles
    contact: ContactInfo
    brand_text: Optional[str] = None
    important_links: BrandLinks
    meta: Dict[str, Any] = {}
