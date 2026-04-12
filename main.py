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

TOKENS = [
    {"id": "arbitrum", "name": "Arbitrum", "symbol": "ARB", "unlock": "92.6M", "date": "Apr 16, 2026", "supply": "10B", "percent": "9.3%", "chain": "Ethereum", "coingecko_id": "arbitrum"},
    {"id": "optimism", "name": "Optimism", "symbol": "OP", "unlock": "24.1M", "date": "Apr 22, 2026", "supply": "4.2B", "percent": "5.7%", "chain": "Ethereum", "coingecko_id": "optimism"},
    {"id": "aptos", "name": "Aptos", "symbol": "APT", "unlock": "11.3M", "date": "May 01, 2026", "supply": "1B", "percent": "1.1%", "chain": "Aptos", "coingecko_id": "aptos"},
    {"id": "sui", "name": "Sui", "symbol": "SUI", "unlock": "64.0M", "date": "May 08, 2026", "supply": "10B", "percent": "6.4%", "chain": "Sui", "coingecko_id": "sui"},
    {"id": "avalanche", "name": "Avalanche", "symbol": "AVAX", "unlock": "8.5M", "date": "May 15, 2026", "supply": "720M", "percent": "1.2%", "chain": "Avalanche", "coingecko_id": "avalanche-2"},
    {"id": "solana", "name": "Solana", "symbol": "SOL", "unlock": "18.2M", "date": "May 20, 2026", "supply": "580M", "percent": "3.1%", "chain": "Solana", "coingecko_id": "solana"},
    {"id": "polygon", "name": "Polygon", "symbol": "MATIC", "unlock": "45.0M", "date": "May 25, 2026", "supply": "10B", "percent": "4.5%", "chain": "Ethereum", "coingecko_id": "matic-network"},
    {"id": "near", "name": "Near", "symbol": "NEAR", "unlock": "22.0M", "date": "Jun 01, 2026", "supply": "1B", "percent": "2.2%", "chain": "Near", "coingecko_id": "near"},
    {"id": "cosmos", "name": "Cosmos", "symbol": "ATOM", "unlock": "12.5M", "date": "Jun 08, 2026", "supply": "390M", "percent": "3.2%", "chain": "Cosmos", "coingecko_id": "cosmos"},
    {"id": "chainlink", "name": "Chainlink", "symbol": "LINK", "unlock": "30.0M", "date": "Jun 15, 2026", "supply": "1B", "percent": "3.0%", "chain": "Ethereum", "coingecko_id": "chainlink"},
    {"id": "uniswap", "name": "Uniswap", "symbol": "UNI", "unlock": "15.0M", "date": "Jun 20, 2026", "supply": "1B", "percent": "1.5%", "chain": "Ethereum", "coingecko_id": "uniswap"},
    {"id": "aave", "name": "Aave", "symbol": "AAVE", "unlock": "5.0M", "date": "Jun 25, 2026", "supply": "16M", "percent": "31.2%", "chain": "Ethereum", "coingecko_id": "aave"},
    {"id": "dydx", "name": "dYdX", "symbol": "DYDX", "unlock": "28.0M", "date": "Jul 01, 2026", "supply": "1B", "percent": "2.8%", "chain": "Cosmos", "coingecko_id": "dydx"},
    {"id": "blur", "name": "Blur", "symbol": "BLUR", "unlock": "200M", "date": "Jul 08, 2026", "supply": "3B", "percent": "6.7%", "chain": "Ethereum", "coingecko_id": "blur"},
    {"id": "starknet", "name": "Starknet", "symbol": "STRK", "unlock": "128M", "date": "Jul 15, 2026", "supply": "10B", "percent": "1.3%", "chain": "Ethereum", "coingecko_id": "starknet"},
    {"id": "celestia", "name": "Celestia", "symbol": "TIA", "unlock": "75.0M", "date": "Jul 20, 2026", "supply": "1B", "percent": "7.5%", "chain": "Celestia", "coingecko_id": "celestia"},
    {"id": "sei", "name": "Sei", "symbol": "SEI", "unlock": "900M", "date": "Jul 25, 2026", "supply": "10B", "percent": "9.0%", "chain": "Sei", "coingecko_id": "sei-network"},
    {"id": "injective", "name": "Injective", "symbol": "INJ", "unlock": "6.0M", "date": "Aug 01, 2026", "supply": "100M", "percent": "6.0%", "chain": "Cosmos", "coingecko_id": "injective-protocol"},
    {"id": "pyth", "name": "Pyth", "symbol": "PYTH", "unlock": "2.1B", "date": "Aug 08, 2026", "supply": "10B", "percent": "21%", "chain": "Solana", "coingecko_id": "pyth-network"},
    {"id": "worldcoin", "name": "Worldcoin", "symbol": "WLD", "unlock": "50.0M", "date": "Aug 15, 2026", "supply": "10B", "percent": "0.5%", "chain": "Ethereum", "coingecko_id": "worldcoin-wld"},
]

@app.get("/")
def root():
    return {"message": "Token Unlock Tracker API", "status": "running", "version": "1.0"}

@app.get("/unlocks")
async def get_unlocks(chain: str = None, search: str = None):
    tokens = TOKENS.copy()
    if chain:
        tokens = [t for t in tokens if t["chain"].lower() == chain.lower()]
    if search:
        tokens = [t for t in tokens if search.lower() in t["name"].lower() or search.lower() in t["symbol"].lower()]
    try:
        ids = ",".join([f"coingecko:{t['coingecko_id']}" for t in tokens])
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://coins.llama.fi/prices/current/{ids}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                coins = data.get("coins", {})
                for token in tokens:
                    key = f"coingecko:{token['coingecko_id']}"
                    price = coins.get(key, {}).get("price")
                    token["price"] = f"${price:.3f}" if price else "N/A"
    except:
        for token in tokens:
            token["price"] = "N/A"
    return {"tokens": tokens, "total": len(tokens)}

@app.get("/unlocks/{token_id}")
async def get_token(token_id: str):
    token = next((t for t in TOKENS if t["id"] == token_id), None)
    if not token:
        return {"error": "Token not found"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://coins.llama.fi/prices/current/coingecko:{token['coingecko_id']}",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                price = data["coins"].get(f"coingecko:{token['coingecko_id']}", {}).get("price")
                token["price"] = f"${price:.3f}" if price else "N/A"
    except:
        token["price"] = "N/A"
    return token

@app.get("/search")
async def search_tokens(q: str = ""):
    tokens = [t for t in TOKENS if q.lower() in t["name"].lower() or q.lower() in t["symbol"].lower()]
    return {"tokens": tokens, "total": len(tokens)}

@app.get("/chains")
def get_chains():
    chains = list(set(t["chain"] for t in TOKENS))
    return {"chains": sorted(chains)}