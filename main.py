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

PROTOCOLS = [
    {"id": "arbitrum", "name": "Arbitrum", "symbol": "ARB", "chain": "Ethereum", "coingecko_id": "arbitrum", "llama_id": "arbitrum"},
    {"id": "optimism", "name": "Optimism", "symbol": "OP", "chain": "Ethereum", "coingecko_id": "optimism", "llama_id": "optimism"},
    {"id": "aptos", "name": "Aptos", "symbol": "APT", "chain": "Aptos", "coingecko_id": "aptos", "llama_id": "aptos"},
    {"id": "sui", "name": "Sui", "symbol": "SUI", "chain": "Sui", "coingecko_id": "sui", "llama_id": "sui"},
    {"id": "avalanche", "name": "Avalanche", "symbol": "AVAX", "chain": "Avalanche", "coingecko_id": "avalanche-2", "llama_id": "avalanche"},
    {"id": "solana", "name": "Solana", "symbol": "SOL", "chain": "Solana", "coingecko_id": "solana", "llama_id": "solana"},
    {"id": "near", "name": "Near", "symbol": "NEAR", "chain": "Near", "coingecko_id": "near", "llama_id": "near"},
    {"id": "cosmos", "name": "Cosmos", "symbol": "ATOM", "chain": "Cosmos", "coingecko_id": "cosmos", "llama_id": "cosmos"},
    {"id": "chainlink", "name": "Chainlink", "symbol": "LINK", "chain": "Ethereum", "coingecko_id": "chainlink", "llama_id": "chainlink"},
    {"id": "uniswap", "name": "Uniswap", "symbol": "UNI", "chain": "Ethereum", "coingecko_id": "uniswap", "llama_id": "uniswap"},
]

STATIC_DATA = {
    "arbitrum": {"unlock": "92.6M", "date": "Apr 16, 2026", "supply": "10B", "percent": "9.3%", "description": "Arbitrum is a Layer 2 scaling solution for Ethereum."},
    "optimism": {"unlock": "24.1M", "date": "Apr 22, 2026", "supply": "4.2B", "percent": "5.7%", "description": "Optimism is a fast, stable L2 blockchain."},
    "aptos": {"unlock": "11.3M", "date": "May 01, 2026", "supply": "1B", "percent": "1.1%", "description": "Aptos is a Layer 1 blockchain."},
    "sui": {"unlock": "64.0M", "date": "May 08, 2026", "supply": "10B", "percent": "6.4%", "description": "Sui is a high throughput Layer 1."},
    "avalanche": {"unlock": "8.5M", "date": "May 15, 2026", "supply": "720M", "percent": "1.2%", "description": "Avalanche is a fast eco-friendly blockchain."},
    "solana": {"unlock": "18.2M", "date": "May 20, 2026", "supply": "580M", "percent": "3.1%", "description": "Solana is a high-performance blockchain."},
    "near": {"unlock": "22.0M", "date": "Jun 01, 2026", "supply": "1B", "percent": "2.2%", "description": "NEAR Protocol is a user-friendly blockchain."},
    "cosmos": {"unlock": "12.5M", "date": "Jun 08, 2026", "supply": "390M", "percent": "3.2%", "description": "Cosmos is an ecosystem of connected blockchains."},
    "chainlink": {"unlock": "30.0M", "date": "Jun 15, 2026", "supply": "1B", "percent": "3.0%", "description": "Chainlink is a decentralized oracle network."},
    "uniswap": {"unlock": "15.0M", "date": "Jun 20, 2026", "supply": "1B", "percent": "1.5%", "description": "Uniswap is the leading decentralized exchange."},
}

async def fetch_prices(coingecko_ids: list):
    try:
        ids = ",".join([f"coingecko:{cid}" for cid in coingecko_ids])
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://coins.llama.fi/prices/current/{ids}",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("coins", {})
    except:
        pass
    return {}

async def fetch_real_unlocks(llama_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.llama.fi/protocol/{llama_id}",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                unlocks = data.get("tokenBreakdowns", {})
                if unlocks:
                    return unlocks
    except:
        pass
    return None

@app.get("/")
def root():
    return {"message": "Token Unlock Tracker API", "status": "running", "version": "2.0"}

@app.get("/unlocks")
async def get_unlocks(chain: str = None, search: str = None):
    protocols = PROTOCOLS.copy()
    if chain and chain != "All":
        protocols = [p for p in protocols if p["chain"].lower() == chain.lower()]
    if search:
        protocols = [p for p in protocols if search.lower() in p["name"].lower() or search.lower() in p["symbol"].lower()]

    coingecko_ids = [p["coingecko_id"] for p in protocols]
    prices = await fetch_prices(coingecko_ids)

    result = []
    for p in protocols:
        static = STATIC_DATA.get(p["id"], {})
        price_key = f"coingecko:{p['coingecko_id']}"
        price = prices.get(price_key, {}).get("price")
        token = {
            **p,
            **static,
            "price": f"${price:.3f}" if price else "N/A",
        }
        result.append(token)

    return {"tokens": result, "total": len(result)}

@app.get("/unlocks/{token_id}")
async def get_token(token_id: str):
    protocol = next((p for p in PROTOCOLS if p["id"] == token_id), None)
    if not protocol:
        return {"error": "Token not found"}

    static = STATIC_DATA.get(token_id, {})
    prices = await fetch_prices([protocol["coingecko_id"]])
    price_key = f"coingecko:{protocol['coingecko_id']}"
    price = prices.get(price_key, {}).get("price")

    return {
        **protocol,
        **static,
        "price": f"${price:.3f}" if price else "N/A",
    }

@app.get("/search")
async def search_tokens(q: str = ""):
    protocols = [p for p in PROTOCOLS if q.lower() in p["name"].lower() or q.lower() in p["symbol"].lower()]
    return {"tokens": protocols, "total": len(protocols)}

@app.get("/chains")
def get_chains():
    chains = list(set(p["chain"] for p in PROTOCOLS))
    return {"chains": sorted(chains)}