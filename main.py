from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def fetch_unlock_data():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.llama.fi/unlocks",
                timeout=15
            )
            if response.status_code == 200:
                return response.json()
    except:
        pass
    return []

async def fetch_prices(coingecko_ids: list):
    try:
        ids = ",".join([f"coingecko:{cid}" for cid in coingecko_ids if cid])
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://coins.llama.fi/prices/current/{ids}",
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get("coins", {})
    except:
        pass
    return {}

async def fetch_price_changes(coingecko_ids: list):
    try:
        ids = ",".join([cid for cid in coingecko_ids if cid])
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
    except:
        pass
    return {}

def format_usd(val):
    if val >= 1e9: return f"${val/1e9:.2f}B"
    if val >= 1e6: return f"${val/1e6:.2f}M"
    if val >= 1e3: return f"${val/1e3:.2f}K"
    return f"${val:.2f}"

def parse_unlock_amount(amount_str):
    try:
        s = str(amount_str).replace(",", "").strip()
        if "B" in s: return float(s.replace("B", "")) * 1e9
        if "M" in s: return float(s.replace("M", "")) * 1e6
        if "K" in s: return float(s.replace("K", "")) * 1e3
        return float(s)
    except:
        return 0

@app.get("/")
def root():
    return {"message": "Token Unlock Tracker API", "status": "running", "version": "4.0"}

@app.get("/unlocks")
async def get_unlocks(chain: str = None, search: str = None):
    try:
        data = await fetch_unlock_data()
        tokens = []

        for item in data:
            try:
                name = item.get("name", "")
                symbol = item.get("symbol", "")
                coingecko_id = item.get("gecko_id", "")
                chain_name = item.get("chain", "")
                logo = item.get("logo", "")

                # Get next unlock event
                events = item.get("events", [])
                if not events:
                    continue

                # Find next upcoming event
                next_event = None
                for event in events:
                    if event.get("timestamp", 0) > 0:
                        next_event = event
                        break

                if not next_event:
                    continue

                # Format date
                import datetime
                timestamp = next_event.get("timestamp", 0)
                date = datetime.datetime.fromtimestamp(timestamp).strftime("%b %d, %Y")

                # Unlock amount
                unlock_amount = next_event.get("noOfTokens", 0)
                if unlock_amount > 1e9:
                    unlock_str = f"{unlock_amount/1e9:.1f}B"
                elif unlock_amount > 1e6:
                    unlock_str = f"{unlock_amount/1e6:.1f}M"
                elif unlock_amount > 1e3:
                    unlock_str = f"{unlock_amount/1e3:.1f}K"
                else:
                    unlock_str = str(unlock_amount)

                # Total supply
                total_supply = item.get("totalLocked", 0)
                if total_supply > 1e9:
                    supply_str = f"{total_supply/1e9:.1f}B"
                elif total_supply > 1e6:
                    supply_str = f"{total_supply/1e6:.1f}M"
                else:
                    supply_str = str(total_supply)

                # Percent of supply
                percent = 0
                if total_supply > 0:
                    percent = (unlock_amount / total_supply) * 100
                percent_str = f"{percent:.1f}%"

                token = {
                    "id": coingecko_id or name.lower().replace(" ", "-"),
                    "name": name,
                    "symbol": symbol,
                    "chain": chain_name,
                    "coingecko_id": coingecko_id,
                    "logo": logo,
                    "unlock": unlock_str,
                    "date": date,
                    "supply": supply_str,
                    "percent": percent_str,
                    "mcap": "N/A",
                    "description": item.get("description", ""),
                    "price": "N/A",
                    "change_24h": 0,
                    "unlock_usd": "N/A",
                }

                # Apply filters
                if chain and chain != "All":
                    if chain_name.lower() != chain.lower():
                        continue
                if search:
                    if search.lower() not in name.lower() and search.lower() not in symbol.lower():
                        continue

                tokens.append(token)
            except:
                continue

        # Fetch prices for all tokens
        coingecko_ids = [t["coingecko_id"] for t in tokens if t["coingecko_id"]]
        if coingecko_ids:
            prices = await fetch_prices(coingecko_ids[:50])
            changes = await fetch_price_changes(coingecko_ids[:50])

            for token in tokens:
                cid = token["coingecko_id"]
                if cid:
                    price_key = f"coingecko:{cid}"
                    price = prices.get(price_key, {}).get("price")
                    change_data = changes.get(cid, {})
                    change_24h = change_data.get("usd_24h_change", 0)

                    if price:
                        token["price"] = f"${price:.3f}"
                        unlock_num = parse_unlock_amount(token["unlock"])
                        unlock_usd = unlock_num * price
                        token["unlock_usd"] = format_usd(unlock_usd)
                        token["change_24h"] = round(change_24h, 2) if change_24h else 0

        return {"tokens": tokens[:100], "total": len(tokens)}

    except Exception as e:
        return {"tokens": [], "total": 0, "error": str(e)}

@app.get("/search")
async def search_tokens(q: str = ""):
    data = await fetch_unlock_data()
    results = []
    for item in data:
        name = item.get("name", "")
        symbol = item.get("symbol", "")
        if q.lower() in name.lower() or q.lower() in symbol.lower():
            results.append({
                "id": item.get("gecko_id", name.lower()),
                "name": name,
                "symbol": symbol,
                "chain": item.get("chain", ""),
                "logo": item.get("logo", ""),
                "coingecko_id": item.get("gecko_id", ""),
                "unlock": "N/A",
                "date": "N/A",
                "price": "N/A",
                "change_24h": 0,
                "unlock_usd": "N/A",
            })
    return {"tokens": results[:20], "total": len(results)}

@app.get("/chains")
async def get_chains():
    data = await fetch_unlock_data()
    chains = list(set(item.get("chain", "") for item in data if item.get("chain")))
    return {"chains": sorted(chains)}