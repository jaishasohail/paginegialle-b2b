from __future__ import annotations

import json
import re
from typing import List, Tuple, Dict, Any, Optional
from bs4 import BeautifulSoup, Tag

from src.utils.helpers import (
    normalize_text,
    safe_float,
    to_phone,
    extract_social_link,
    default_record,
)

class PagineGialleParser:
    """
    Parser tuned for PagineGialle result and detail pages.
    Uses resilient selectors with graceful fallbacks.
    """

    def parse_listing_links_and_next(self, html: str, base_url: str) -> Tuple[List[str], Optional[str]]:
        """
        From a search result page, extract business profile links and the next page URL.
        """
        soup = BeautifulSoup(html, "lxml")

        # Links to company pages
        links: List[str] = []
        for a in soup.select('a[href*="/scheda/"], a[href*="/azienda/"], a[href*="/profilo/"]'):
            href = a.get("href")
            if not href:
                continue
            # Ensure absolute
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = "https://www.paginegialle.it" + href
            if href not in links:
                links.append(href)

        # Next page
        next_url = None
        nxt = soup.select_one('a[rel="next"], a.next, a.pagination-next, li.next > a')
        if nxt and nxt.get("href"):
            href = nxt.get("href")
            if href.startswith("//"):
                next_url = "https:" + href
            elif href.startswith("/"):
                next_url = "https://www.paginegialle.it" + href
            else:
                next_url = href

        return links, next_url

    def parse_detail(self, html: str) -> Dict[str, Any]:
        """
        Parse a business detail page into a normalized record.
        """
        soup = BeautifulSoup(html, "lxml")
        rec = default_record()

        # Business name
        name = soup.select_one("h1, h1[itemprop='name'], .company-name, .title h1")
        rec["businessName"] = normalize_text(name.get_text(strip=True)) if name else None

        # Address
        addr = soup.select_one("address, .address, .indirizzo, [itemprop='address']")
        rec["address"] = normalize_text(addr.get_text(" ", strip=True)) if addr else None

        # Phone
        phone = None
        phone_el = soup.select_one("a[href^='tel:'], .phone, [itemprop='telephone']")
        if phone_el:
            phone = phone_el.get("href") or phone_el.get_text(" ", strip=True)
        rec["phoneNumber"] = to_phone(phone)

        # Website & email
        website = None
        email = None
        links = []
        for a in soup.select("a[href]"):
            href = a["href"]
            links.append(href)
            if href.startswith("http") and "paginegialle.it" not in href:
                # Heuristic: the first external http link is likely website
                website = website or href
            if href.startswith("mailto:"):
                email = email or href.replace("mailto:", "").split("?")[0]
            if href.startswith("https://wa.me/") or "api.whatsapp.com" in href:
                rec["whatsapp"] = href

        rec["website"] = website
        rec["email"] = email

        # Rating / reviews
        rating = None
        reviews = None
        rt = soup.select_one('[itemprop="ratingValue"], .rating .value, .rating-value')
        if rt:
            rating = safe_float(rt.get_text(strip=True))
        rc = soup.select_one('[itemprop="reviewCount"], .reviews-count, .review-count')
        if rc:
            try:
                reviews = int(re.sub(r"[^\d]", "", rc.get_text()))
            except Exception:
                reviews = None
        rec["rating"] = rating
        rec["reviews_count"] = reviews

        # Social links
        rec["facebook"] = extract_social_link(links, "facebook.com")
        rec["instagram"] = extract_social_link(links, "instagram.com")
        rec["twitter"] = extract_social_link(links, "twitter.com")

        # Geo data (if embedded as JSON-LD)
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, list):
                    for d in data:
                        self._apply_jsonld(d, rec)
                elif isinstance(data, dict):
                    self._apply_jsonld(data, rec)
            except Exception:
                continue

        # Zip/City/Province heuristics from address text when not present
        if rec["address"] and not rec["zip_code"]:
            m = re.search(r"\b(\d{5})\b", rec["address"])
            if m:
                rec["zip_code"] = m.group(1)
        if rec["address"] and not rec["city"]:
            m = re.search(r"\b([A-ZÀ-ÖØ-Ýa-zà-öø-ÿ'’\-\s]{2,})\s*(?:\(|,|\d|$)", rec["address"])
            if m:
                rec["city"] = normalize_text(m.group(1))
        if rec["address"] and not rec["province"]:
            m = re.search(r"\b([A-Z]{2})\b", rec["address"])
            if m:
                rec["province"] = m.group(1)

        # Opening hours (raw JSON if present in JSON-LD)
        # Description
        desc = soup.select_one("meta[name='description']") or soup.select_one("p.description, .descrizione")
        if desc:
            rec["description"] = normalize_text(desc.get("content") or desc.get_text(" ", strip=True))

        return rec

    def _apply_jsonld(self, data: Dict[str, Any], rec: Dict[str, Any]) -> None:
        # Organization / LocalBusiness structure
        if "@type" in data and isinstance(data["@type"], (str, list)):
            addr = data.get("address", {})
            if isinstance(addr, dict):
                rec["zip_code"] = rec["zip_code"] or addr.get("postalCode")
                rec["city"] = rec["city"] or addr.get("addressLocality")
                rec["province"] = rec["province"] or addr.get("addressRegion")
                # as a fallback for address
                street = " ".join(
                    [x for x in [addr.get("streetAddress"), addr.get("addressLocality"), addr.get("postalCode")] if x]
                ).strip()
                rec["address"] = rec["address"] or (street if street else None)

            geo = data.get("geo", {})
            if isinstance(geo, dict):
                rec["latitude"] = rec["latitude"] || geo.get("latitude")
                rec["longitude"] = rec["longitude"] || geo.get("longitude")

        # Opening hours
        opening = data.get("openingHoursSpecification")
        if opening:
            try:
                rec["opening_hours"] = json.dumps(opening, ensure_ascii=False)
            except Exception:
                pass