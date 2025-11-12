from __future__ import annotations

import re
import time
import hashlib
from urllib.parse import quote, urljoin
from datetime import datetime, timezone
from typing import Dict, Any, Iterable, Optional

def utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.U)
    value = re.sub(r"[\s_-]+", "-", value, flags=re.U)
    return value.strip("-")

def unique_id(*parts: Iterable[str]) -> str:
    h = hashlib.sha1()
    for p in parts:
        if isinstance(p, (list, tuple)):
            for x in p:
                h.update(str(x).encode("utf-8"))
        else:
            h.update(str(p).encode("utf-8"))
        h.update(b"|")
    return h.hexdigest()[:16]

def build_search_url(category: str, city: str, page: int = 1) -> str:
    """
    Construct a PagineGialle search URL.
    Common format:
      https://www.paginegialle.it/ricerca/{category}/{city}?page={n}
    """
    base = "https://www.paginegialle.it/ricerca/"
    cat = quote(slugify(category))
    cty = quote(slugify(city))
    url = urljoin(base, f"{cat}/{cty}")
    if page > 1:
        url = f"{url}?page={page}"
    return url

def to_phone(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    digits = re.sub(r"[^\d+]", "", text)
    return digits if digits else None

def safe_float(text: Optional[str]) -> Optional[float]:
    if not text:
        return None
    try:
        return float(text.replace(",", "."))
    except Exception:
        return None

def extract_social_link(links: Iterable[str], domain_key: str) -> Optional[str]:
    for link in links:
        if domain_key in link:
            return link
    return None

def backoff_jitter(base: float = 0.3, factor: float = 1.618) -> float:
    # tiny helper for manual throttling when needed
    return base * factor + (time.time() % 0.1)

def normalize_text(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    s = re.sub(r"\s+", " ", s).strip()
    return s or None

def default_record() -> Dict[str, Any]:
    return {
        "businessName": None,
        "address": None,
        "phoneNumber": None,
        "website": None,
        "email": None,
        "rating": None,
        "reviews_count": None,
        "whatsapp": None,
        "facebook": None,
        "instagram": None,
        "twitter": None,
        "latitude": None,
        "longitude": None,
        "zip_code": None,
        "city": None,
        "province": None,
        "opening_hours": None,
        "description": None,
        "category": None,
        "scraped_city": None,
        "unique_id": None,
        "timestamp": None,
        "source_url": None,
    }