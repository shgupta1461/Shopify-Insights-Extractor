import re
from typing import Iterable, List, Tuple
from bs4 import BeautifulSoup

# Regex patterns
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")

# Social media detection keywords
SOCIAL_KEYS = {
    "instagram": "instagram.com",
    "facebook": "facebook.com",
    "tiktok": "tiktok.com",
    "twitter": "twitter.com|x.com",
    "youtube": "youtube.com|youtu.be",
    "pinterest": "pinterest.com",
    "linkedin": "linkedin.com",
}

# Policy keywords
POLICY_KEYWORDS = {
    "privacy": ["privacy"],
    "returns": ["return", "refund", "exchange"],
}

# Important brand links
IMPORTANT_LINKS = {
    "contact_us": ["contact"],
    "order_tracking": ["track", "tracking", "order status"],
    "blog": ["blog"],
    "about": ["about"],
}

# Extractors
def find_emails(text: str) -> List[str]:
    return sorted(set(EMAIL_RE.findall(text or "")))

def find_phones(text: str) -> List[str]:
    return sorted(set(PHONE_RE.findall(text or "")))

def absolute_url(base: str, href: str) -> str:
    from urllib.parse import urljoin
    return urljoin(base, href)

def find_links_by_keywords(base_url: str, soup: BeautifulSoup, keywords: Iterable[str]) -> List[Tuple[str, str]]:
    results = []
    for a in soup.select('a[href]'):
        text = (a.get_text(" ") or "").strip().lower()
        href = a['href']
        hay = f"{text} {href}".lower()
        if any(k in hay for k in keywords):
            results.append((text, absolute_url(base_url, href)))
    return results

def pick_first_url(links: List[Tuple[str, str]]):
    return links[0][1] if links else None

def text_snippet(s: str, n: int = 500) -> str:
    s = (s or "").strip()
    return (s[:n] + "…") if len(s) > n else s
