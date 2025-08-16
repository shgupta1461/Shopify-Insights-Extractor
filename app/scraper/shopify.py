# import re
# from typing import Iterable, List, Tuple
# from bs4 import BeautifulSoup

# # Regex patterns
# EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")

# class ShopifyScraper:
#     def __init__(self, base_url: str):
#         self.base_url = base_url

#     def scrape(self):
#         # Implement scraping logic here
#         # For example, fetch the page and parse with BeautifulSoup
#         pass


# # Social media detection keywords
# SOCIAL_KEYS = {
#     "instagram": "instagram.com",
#     "facebook": "facebook.com",
#     "tiktok": "tiktok.com",
#     "twitter": "twitter.com|x.com",
#     "youtube": "youtube.com|youtu.be",
#     "pinterest": "pinterest.com",
#     "linkedin": "linkedin.com",
# }

# # Policy keywords
# POLICY_KEYWORDS = {
#     "privacy": ["privacy"],
#     "returns": ["return", "refund", "exchange"],
# }

# # Important brand links
# IMPORTANT_LINKS = {
#     "contact_us": ["contact"],
#     "order_tracking": ["track", "tracking", "order status"],
#     "blog": ["blog"],
#     "about": ["about"],
# }

# # Extractors
# def find_emails(text: str) -> List[str]:
#     return sorted(set(EMAIL_RE.findall(text or "")))

# def find_phones(text: str) -> List[str]:
#     return sorted(set(PHONE_RE.findall(text or "")))

# def absolute_url(base: str, href: str) -> str:
#     from urllib.parse import urljoin
#     return urljoin(base, href)

# def find_links_by_keywords(base_url: str, soup: BeautifulSoup, keywords: Iterable[str]) -> List[Tuple[str, str]]:
#     results = []
#     for a in soup.select('a[href]'):
#         text = (a.get_text(" ") or "").strip().lower()
#         href = a['href']
#         hay = f"{text} {href}".lower()
#         if any(k in hay for k in keywords):
#             results.append((text, absolute_url(base_url, href)))
#     return results

# def pick_first_url(links: List[Tuple[str, str]]):
#     return links[0][1] if links else None

# def text_snippet(s: str, n: int = 500) -> str:
#     s = (s or "").strip()
#     return (s[:n] + "…") if len(s) > n else s







import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

from .common import (
    find_emails,
    find_phones,
    find_links_by_keywords,
    SOCIAL_KEYS,
    POLICY_KEYWORDS,
    IMPORTANT_LINKS,
)

class ShopifyScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def scrape(self) -> Dict[str, Any]:
        result = {}
        try:
            # 1. Fetch homepage
            resp = requests.get(self.base_url, timeout=10)
            if resp.status_code == 404:
                return {"error": "404 Not Found"}
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(" ", strip=True)

            # 2. Product Catalog
            products_url = self.base_url.rstrip("/") + "/products.json"
            products = []
            try:
                prod_resp = requests.get(products_url, timeout=10)
                if prod_resp.ok:
                    prod_json = prod_resp.json()
                    products = prod_json.get("products", [])
            except Exception:
                pass
            result["product_catalog"] = products

            # 3. Hero Products (from homepage)
            hero_products = []
            for a in soup.find_all("a", href=True):
                if "/products/" in a["href"]:
                    hero_products.append(a["href"])
            result["hero_products"] = list(set(hero_products))

            # 4. Policies
            for key, keywords in POLICY_KEYWORDS.items():
                links = find_links_by_keywords(self.base_url, soup, keywords)
                result[f"{key}_policy_links"] = links

            # 5. FAQs
            faqs = []
            #faq_sections = soup.find_all(lambda tag: tag.name in ["section", "div"] and "faq" in (tag.get("id", "") + tag.get("class", "")).lower())
            faq_sections = soup.find_all(
                    lambda tag: tag.name in ["section", "div"] and
                    "faq" in (
                        (tag.get("id", "") or "") +
                        " ".join(tag.get("class", []) or [])
                    ).lower()
                )
            
            for section in faq_sections:
                qas = []
                for q in section.find_all(["h2", "h3", "strong"]):
                    question = q.get_text(strip=True)
                    answer = q.find_next_sibling(text=True)
                    if question and answer:
                        qas.append({"question": question, "answer": answer.strip()})
                faqs.extend(qas)
            result["faqs"] = faqs

            # 6. Social Handles
            social_links = {}
            for key, pattern in SOCIAL_KEYS.items():
                links = find_links_by_keywords(self.base_url, soup, [pattern])
                social_links[key] = links
            result["social_links"] = social_links

            # 7. Contact Details
            result["emails"] = find_emails(text)
            result["phones"] = find_phones(text)

            # 8. Brand Context (About)
            about_links = find_links_by_keywords(self.base_url, soup, ["about"])
            result["about_links"] = about_links

            # 9. Important Links
            important = {}
            for key, keywords in IMPORTANT_LINKS.items():
                links = find_links_by_keywords(self.base_url, soup, keywords)
                important[key] = links
            result["important_links"] = important

            return result
        except Exception as e:
            return {"error": str(e)}
    

def scrape_shopify_data(base_url: str):
    scraper = ShopifyScraper(base_url)
    return scraper.scrape()










# import requests
# from bs4 import BeautifulSoup
# from .common import find_emails, find_phones, find_links_by_keywords, SOCIAL_KEYS, POLICY_KEYWORDS, IMPORTANT_LINKS

# def scrape_shopify_data(base_url: str):
#     result = {}
#     try:
#         # 1. Fetch homepage
#         resp = requests.get(base_url, timeout=10)
#         if resp.status_code == 404:
#             return {"error": "404 Not Found"}
#         resp.raise_for_status()
#         soup = BeautifulSoup(resp.text, "html.parser")
#         text = soup.get_text(" ", strip=True)

#         # 2. Product Catalog
#         products_url = base_url.rstrip("/") + "/products.json"
#         products = []
#         try:
#             prod_resp = requests.get(products_url, timeout=10)
#             if prod_resp.ok:
#                 prod_json = prod_resp.json()
#                 products = prod_json.get("products", [])
#         except Exception:
#             pass
#         result["product_catalog"] = products

#         # 3. Hero Products (from homepage)
#         hero_products = []
#         for a in soup.find_all("a", href=True):
#             if "/products/" in a["href"]:
#                 hero_products.append(a["href"])
#         result["hero_products"] = list(set(hero_products))

#         # 4. Policies
#         for key, keywords in POLICY_KEYWORDS.items():
#             links = find_links_by_keywords(base_url, soup, keywords)
#             result[f"{key}_policy_links"] = links

#         # 5. FAQs
#         faqs = []
#         faq_sections = soup.find_all(lambda tag: tag.name in ["section", "div"] and "faq" in (tag.get("id", "") + tag.get("class", "")).lower())
#         for section in faq_sections:
#             qas = []
#             for q in section.find_all(["h2", "h3", "strong"]):
#                 question = q.get_text(strip=True)
#                 answer = q.find_next_sibling(text=True)
#                 if question and answer:
#                     qas.append({"question": question, "answer": answer.strip()})
#             faqs.extend(qas)
#         result["faqs"] = faqs

#         # 6. Social Handles
#         social_links = {}
#         for key, pattern in SOCIAL_KEYS.items():
#             links = find_links_by_keywords(base_url, soup, [pattern])
#             social_links[key] = links
#         result["social_links"] = social_links

#         # 7. Contact Details
#         result["emails"] = find_emails(text)
#         result["phones"] = find_phones(text)

#         # 8. Brand Context (About)
#         about_links = find_links_by_keywords(base_url, soup, ["about"])
#         result["about_links"] = about_links

#         # 9. Important Links
#         important = {}
#         for key, keywords in IMPORTANT_LINKS.items():
#             links = find_links_by_keywords(base_url, soup, keywords)
#             important[key] = links
#         result["important_links"] = important

#         return result
#     except Exception as e:
#         return {"error": str(e)}