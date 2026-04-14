import sys
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import re
import logging
import httpx
import json
import os
import subprocess
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Token Unlock Tracker API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_cache = {"tokens": [], "last_updated": None, "is_loading": False, "source": "none"}


def load_tokens_from_file() -> list:
    """Load tokens from all_tokens.json file."""
    try:
        with open("all_tokens.json") as f:
            tokens = json.load(f)
        logger.info(f"✅ Loaded {len(tokens)} tokens from all_tokens.json")
        return tokens
    except Exception as e:
        logger.warning(f"Could not load all_tokens.json: {e}")
        return []


def fmt_large(n) -> str:
    try:
        n = float(n)
        if n >= 1e9: return f"{n/1e9:.2f}B"
        if n >= 1e6: return f"{n/1e6:.2f}M"
        if n >= 1e3: return f"{n/1e3:.2f}K"
        return f"{n:.4f}"
    except Exception:
        return str(n)


async def fetch_coingecko_prices(ids: list) -> dict:
    prices = {}
    async with httpx.AsyncClient(timeout=15) as client:
        for i in range(0, len(ids), 100):
            chunk = ",".join(ids[i:i+100])
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={chunk}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
            try:
                r = await client.get(url)
                if r.status_code == 200:
                    prices.update(r.json())
                    logger.info(f"  CoinGecko: +{len(r.json())} prices")
            except Exception as e:
                logger.warning(f"CoinGecko error: {e}")
            await asyncio.sleep(1.5)
    return prices


def enrich_with_prices(tokens: list, prices: dict) -> list:
    for t in tokens:
        cg = t.get("coingecko_id", "")
        if cg and cg in prices:
            p = prices[cg]
            t["price"] = p.get("usd", t.get("price", 0))
            t["change_24h"] = round(float(p.get("usd_24h_change") or 0), 2)
            mc = p.get("usd_market_cap", 0)
            if mc:
                t["mcap"] = f"${fmt_large(mc)}"
            try:
                s = t.get("unlock", "0").replace("B","e9").replace("M","e6").replace("K","e3")
                n = float(re.sub(r'[^\d.e\-]', '', s))
                t["unlock_usd"] = round(n * t["price"], 2)
            except Exception:
                pass
    return tokens


async def update_cache():
    global _cache
    if _cache["is_loading"]:
        return
    _cache["is_loading"] = True
    logger.info("🚀 Loading tokens...")

    # Load from file
    tokens = load_tokens_from_file()

    if not tokens:
        logger.warning("No tokens found!")
        _cache["is_loading"] = False
        return

    # Enrich with live CoinGecko prices
    logger.info(f"💰 Getting live prices for {len(tokens)} tokens...")
    ids = list({t["coingecko_id"] for t in tokens if t.get("coingecko_id")})
    prices = await fetch_coingecko_prices(ids)
    tokens = enrich_with_prices(tokens, prices)

    # Sort by date
    def sort_key(t):
        try:
            return datetime.strptime(t["date"], "%b %d, %Y")
        except Exception:
            return datetime(2099, 1, 1)

    tokens.sort(key=sort_key)
    _cache.update({
        "tokens": tokens,
        "last_updated": datetime.now().isoformat(),
        "is_loading": False,
        "source": "dropstab"
    })
    logger.info(f"✅ Done! {len(tokens)} tokens ready!")


async def periodic_refresh():
    """Refresh prices every 5 minutes."""
    while True:
        await asyncio.sleep(5 * 60)
        await update_cache()


@app.on_event("startup")
async def startup():
    asyncio.create_task(update_cache())
    asyncio.create_task(periodic_refresh())


@app.get("/")
def root():
    return {"status": "ok", "tokens": len(_cache["tokens"]),
            "last_updated": _cache["last_updated"], "source": _cache["source"]}


@app.get("/tokens")
def get_tokens(page: int = 1, limit: int = 50, search: str = "", sort: str = "date"):
    tokens = _cache["tokens"]
    if not tokens:
        return {"tokens": [], "total": 0, "loading": True}
    if search:
        q = search.lower()
        tokens = [t for t in tokens if q in t["name"].lower() or q in t["symbol"].lower()]
    if sort == "unlock_usd":
        tokens = sorted(tokens, key=lambda t: t.get("unlock_usd", 0), reverse=True)
    elif sort == "change":
        tokens = sorted(tokens, key=lambda t: t.get("change_24h", 0), reverse=True)
    total = len(tokens)
    s = (page - 1) * limit
    return {"tokens": tokens[s:s+limit], "total": total, "page": page,
            "limit": limit, "last_updated": _cache["last_updated"],
            "source": _cache["source"]}


@app.get("/tokens/{token_id}")
def get_token(token_id: str):
    for t in _cache["tokens"]:
        if t["id"] == token_id:
            return t
    return {"error": "not found"}


@app.post("/refresh")
async def manual_refresh(bg: BackgroundTasks):
    bg.add_task(update_cache)
    return {"status": "refresh started"}


@app.get("/status")
def status():
    return {"total_tokens": len(_cache["tokens"]),
            "last_updated": _cache["last_updated"],
            "loading": _cache["is_loading"],
            "source": _cache["source"]}