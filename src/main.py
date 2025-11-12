from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import ujson
from pydantic import BaseModel, Field

from src.scraper.request_handler import RequestHandler
from src.scraper.paginegialle_parser import PagineGialleParser
from src.utils.helpers import (
    build_search_url,
    unique_id,
    utc_iso,
    backoff_jitter,
    default_record,
    normalize_text,
)
from src.utils.logger import get_logger

class InputConfig(BaseModel):
    categories: List[str] = Field(default_factory=list)
    cities: List[str] = Field(default_factory=list)
    filterByEmail: bool = False
    filterByPhone: bool = False

class Settings(BaseModel):
    concurrency: int = 8
    proxy: Optional[str] = None
    request_headers: Dict[str, str] = Field(default_factory=dict)
    max_pages_per_combo: int = 50
    sleep_between_requests_ms: int = 150

logger = get_logger("main")

async def scrape_combo(
    handler: RequestHandler,
    parser: PagineGialleParser,
    category: str,
    city: str,
    settings: Settings,
) -> List[Dict[str, Any]]:
    """
    Scrape a (category, city) combination with smart pagination.
    """
    results: List[Dict[str, Any]] = []
    seen_detail_urls: set[str] = set()

    # Crawl listing pages
    listing_urls: List[str] = []
    page = 1
    next_url: Optional[str] = build_search_url(category, city, page=page)

    while next_url and page <= settings.max_pages_per_combo:
        html = await handler.fetch_text(next_url)
        if not html:
            break
        links, nxt = parser.parse_listing_links_and_next(html, base_url=next_url)
        logger.info(f"[{category}/{city}] page {page} -> {len(links)} links")
        listing_urls.extend([u for u in links if u not in seen_detail_urls])
        next_url = nxt
        page += 1
        # light throttle
        await asyncio.sleep(settings.sleep_between_requests_ms / 1000.0 + backoff_jitter())

    # Deduplicate
    detail_urls = list(dict.fromkeys(listing_urls))

    # Fetch details concurrently
    fetched = await handler.gather_texts(detail_urls)

    for url, html in fetched.items():
        if not html:
            continue
        rec = parser.parse_detail(html)

        # fill search context
        rec["category"] = normalize_text(category)
        rec["scraped_city"] = normalize_text(city)
        rec["source_url"] = url
        rec["timestamp"] = utc_iso()
        rec["unique_id"] = unique_id("pg", category, city, rec.get("businessName") or url)

        results.append(rec)

    return results

def apply_filters(
    rows: List[Dict[str, Any]],
    *,
    email: bool,
    phone: bool,
) -> List[Dict[str, Any]]:
    if not email and not phone:
        return rows
    out: List[Dict[str, Any]] = []
    for r in rows:
        if email and not r.get("email"):
            continue
        if phone and not r.get("phoneNumber"):
            continue
        out.append(r)
    return out

async def run(input_path: Path, output_path: Optional[Path]) -> List[Dict[str, Any]]:
    # Load input & settings
    root = Path(__file__).resolve().parents[1]
    settings_path = root / "src" / "config" / "settings.json"
    with settings_path.open("r", encoding="utf-8") as f:
        settings = Settings.model_validate_json(f.read())

    with input_path.open("r", encoding="utf-8") as f:
        inp = InputConfig.model_validate_json(f.read())

    handler = RequestHandler(
        base_headers=settings.request_headers,
        proxy=settings.proxy,
        concurrency=settings.concurrency,
    )
    parser = PagineGialleParser()

    all_results: List[Dict[str, Any]] = []

    try:
        combos = [(c, t) for c in inp.categories for t in inp.cities]
        if not combos:
            logger.warning("No categories/cities provided. Nothing to do.")
            return []

        logger.info(f"Starting scrape: {len(combos)} combinations, concurrency={settings.concurrency}")

        for cat, city in combos:
            try:
                combo_results = await scrape_combo(handler, parser, cat, city, settings)
                all_results.extend(combo_results)
            except Exception as e:
                logger.error(f"Combo failed {cat}/{city}: {e}")

        # Filters
        all_results = apply_filters(all_results, email=inp.filterByEmail, phone=inp.filterByPhone)

        # Persist
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            logger.info(f"Wrote {len(all_results)} records to {output_path}")
        else:
            print(ujson.dumps(all_results, ensure_ascii=False, indent=2))

    finally:
        await handler.close()

    return all_results

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="PagineGialle.it B2B Scraper")
    p.add_argument(
        "--input",
        "-i",
        type=Path,
        default=Path("data/sample_input.json"),
        help="Path to input configuration JSON",
    )
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("data/output.json"),
        help="Where to write JSON results. If omitted, prints to stdout.",
    )
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run(args.input, args.output))
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")