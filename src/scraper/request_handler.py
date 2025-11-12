from __future__ import annotations

import asyncio
import random
from typing import Optional, Dict, Any, List

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from src.utils.logger import get_logger

DEFAULT_TIMEOUT = httpx.Timeout(20.0, read=30.0, connect=20.0)
USER_AGENTS: List[str] = [
    # A small rotating pool; callers can extend via settings if desired.
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
]

class RequestHandler:
    """
    Async HTTP client with retries, proxy and header support.
    """

    def __init__(
        self,
        *,
        base_headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
        concurrency: int = 8,
        timeout: httpx.Timeout = DEFAULT_TIMEOUT,
    ) -> None:
        self.logger = get_logger("request")
        self.semaphore = asyncio.Semaphore(concurrency)
        self.proxy = proxy
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
        }
        if base_headers:
            headers.update(base_headers)
        self._headers = headers
        self._client = httpx.AsyncClient(
            headers=self._headers,
            timeout=timeout,
            proxies=self.proxy,
            http2=True,
            follow_redirects=True,
        )

    async def close(self) -> None:
        await self._client.aclose()

    def _with_random_ua(self) -> Dict[str, str]:
        h = dict(self._headers)
        h["User-Agent"] = random.choice(USER_AGENTS)
        return h

    @retry(stop=stop_after_attempt(4), wait=wait_exponential_jitter(initial=0.5, max=5))
    async def get(self, url: str) -> httpx.Response:
        async with self.semaphore:
            self.logger.debug(f"GET {url}")
            resp = await self._client.get(url, headers=self._with_random_ua())
            # Simple anti-bot: some sites respond 403 sporadically; retry those.
            if resp.status_code in (403, 429, 500, 502, 503, 504):
                self.logger.warning(f"Retryable status {resp.status_code} for {url}")
                raise httpx.HTTPStatusError("Retryable status", request=resp.request, response=resp)
            return resp

    async def fetch_text(self, url: str) -> Optional[str]:
        try:
            r = await self.get(url)
            ctype = r.headers.get("Content-Type", "")
            if "text/html" in ctype or "application/xhtml+xml" in ctype:
                return r.text
            return r.text  # fallback; many servers forget correct header
        except Exception as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            return None

    async def gather_texts(self, urls: List[str]) -> Dict[str, Optional[str]]:
        results: Dict[str, Optional[str]] = {}
        async def _one(u: str):
            results[u] = await self.fetch_text(u)
        await asyncio.gather(*[_one(u) for u in urls])
        return results