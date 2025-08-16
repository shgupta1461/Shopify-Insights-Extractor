from typing import Dict
from fastapi import HTTPException
from ..schemas import BrandContext, Product, SocialHandles, ContactInfo, BrandLinks, Policy, FAQ
from ..scraper.shopify import ShopifyScraper

# Normalize raw Shopify product JSON → Product schema
def normalize_products(raw_products):
    products = []
    for p in raw_products:
        variants = p.get('variants') or []
        price = None
        currency = None
        if variants:
            try:
                price = float(variants[0].get('price')) if variants[0].get('price') is not None else None
            except Exception:
                price = None
        images = [img.get('src') for img in (p.get('images') or []) if img.get('src')]
        products.append(Product(
            id=str(p.get('id') or ''),
            handle=p.get('handle'),
            title=p.get('title'),
            price=price,
            currency=currency,
            url=None,
            images=images or None,
        ))
    return products

# Normalize hero products
def normalize_hero(raw):
    out = []
    for r in raw:
        out.append(Product(title=r.get('title'), url=r.get('url')))
    return out

# Core extractor
def extract_brand_context(website_url: str) -> BrandContext:
    try:
        scraper = ShopifyScraper(website_url)
        brand_name = scraper.fetch_brand_name()
        catalog_raw = scraper.fetch_catalog()
        hero_raw = scraper.fetch_hero_products()
        policies_raw = scraper.fetch_policies()
        faqs_raw = scraper.fetch_faqs()
        social_raw = scraper.fetch_social()
        contact_raw = scraper.fetch_contact()
        brand_text, links_raw = scraper.fetch_brand_text_and_links()
    except Exception as e:
        # Raise 401 if unreachable, per assignment spec
        raise HTTPException(status_code=401, detail=f"Website not found or unreachable: {e}")

    # Build structured objects
    policies = [Policy(**p) for p in policies_raw]
    faqs = [FAQ(**q) for q in faqs_raw]
    social = SocialHandles(**social_raw)
    contact = ContactInfo(**contact_raw)
    links = BrandLinks(**links_raw)
    catalog = normalize_products(catalog_raw)
    hero = normalize_hero(hero_raw)

    meta: Dict[str, str] = {
        "generator": "Shopify Insights Fetcher",
    }

    return BrandContext(
        website_url=website_url,
        brand_name=brand_name,
        whole_product_catalog=catalog,
        hero_products=hero,
        policies=policies,
        faqs=faqs,
        social_handles=social,
        contact=contact,
        brand_text=brand_text,
        important_links=links,
        meta=meta,
    )
