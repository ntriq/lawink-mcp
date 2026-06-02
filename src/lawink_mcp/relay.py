"""ntriq-platform 백엔드 HTTP relay (httpx async)."""
import httpx

from . import config


def _headers() -> dict:
    h = {"Accept": "application/json"}
    if config.API_KEY:
        h["X-API-Key"] = config.API_KEY
    return h


async def get(path: str, params: dict | None = None) -> dict:
    """GET {API_BASE}{API_PREFIX}{path}. 온톨로지 조회용."""
    url = f"{config.API_BASE}{config.API_PREFIX}{path}"
    async with httpx.AsyncClient(timeout=config.TIMEOUT) as client:
        resp = await client.get(url, params=params or {}, headers=_headers())
        resp.raise_for_status()
        return resp.json()


async def post(path: str, body: dict | None = None) -> dict:
    """POST {API_BASE}{API_PREFIX}{path}. 시맨틱검색용."""
    url = f"{config.API_BASE}{config.API_PREFIX}{path}"
    async with httpx.AsyncClient(timeout=config.TIMEOUT) as client:
        resp = await client.post(url, json=body or {}, headers=_headers())
        resp.raise_for_status()
        return resp.json()
