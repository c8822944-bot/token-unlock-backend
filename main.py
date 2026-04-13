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
    {"id": "arbitrum", "name": "Arbitrum", "symbol": "ARB", "chain": "Ethereum", "coingecko_id": "arbitrum", "logo": "https://assets.coingecko.com/coins/images/16547/large/photo_2023-03-29_21.47.00.jpeg"},
    {"id": "optimism", "name": "Optimism", "symbol": "OP", "chain": "Ethereum", "coingecko_id": "optimism", "logo": "https://assets.coingecko.com/coins/images/25244/large/Optimism.png"},
    {"id": "aptos", "name": "Aptos", "symbol": "APT", "chain": "Aptos", "coingecko_id": "aptos", "logo": "https://assets.coingecko.com/coins/images/26455/large/aptos_round.png"},
    {"id": "sui", "name": "Sui", "symbol": "SUI", "chain": "Sui", "coingecko_id": "sui", "logo": "https://assets.coingecko.com/coins/images/26375/large/sui-ocean-square.png"},
    {"id": "avalanche", "name": "Avalanche", "symbol": "AVAX", "chain": "Avalanche", "coingecko_id": "avalanche-2", "logo": "https://assets.coingecko.com/coins/images/12559/large/Avalanche_Circle_RedWhite_Trans.png"},
    {"id": "solana", "name": "Solana", "symbol": "SOL", "chain": "Solana", "coingecko_id": "solana", "logo": "https://assets.coingecko.com/coins/images/4128/large/solana.png"},
    {"id": "near", "name": "Near", "symbol": "NEAR", "chain": "Near", "coingecko_id": "near", "logo": "https://assets.coingecko.com/coins/images/10365/large/near.jpg"},
    {"id": "cosmos", "name": "Cosmos", "symbol": "ATOM", "chain": "Cosmos", "coingecko_id": "cosmos", "logo": "https://assets.coingecko.com/coins/images/1481/large/cosmos_hub.png"},
    {"id": "chainlink", "name": "Chainlink", "symbol": "LINK", "chain": "Ethereum", "coingecko_id": "chainlink", "logo": "https://assets.coingecko.com/coins/images/877/large/chainlink-new-logo.png"},
    {"id": "uniswap", "name": "Uniswap", "symbol": "UNI", "chain": "Ethereum", "coingecko_id": "uniswap", "logo": "https://assets.coingecko.com/coins/images/12504/large/uni.jpg"},
    {"id": "aave", "name": "Aave", "symbol": "AAVE", "chain": "Ethereum", "coingecko_id": "aave", "logo": "https://assets.coingecko.com/coins/images/12645/large/AAVE.png"},
    {"id": "polygon", "name": "Polygon", "symbol": "MATIC", "chain": "Ethereum", "coingecko_id": "matic-network", "logo": "https://assets.coingecko.com/coins/images/4713/large/matic-token-icon.png"},
    {"id": "starknet", "name": "Starknet", "symbol": "STRK", "chain": "Ethereum", "coingecko_id": "starknet", "logo": "https://assets.coingecko.com/coins/images/26433/large/starknet.png"},
    {"id": "celestia", "name": "Celestia", "symbol": "TIA", "chain": "Celestia", "coingecko_id": "celestia", "logo": "https://assets.coingecko.com/coins/images/31967/large/tia.jpg"},
    {"id": "sei", "name": "Sei", "symbol": "SEI", "chain": "Sei", "coingecko_id": "sei-network", "logo": "https://assets.coingecko.com/coins/images/28205/large/Sei_Logo_-_Transparent.png"},
    {"id": "injective", "name": "Injective", "symbol": "INJ", "chain": "Cosmos", "coingecko_id": "injective-protocol", "logo": "https://assets.coingecko.com/coins/images/12882/large/Secondary_Symbol.png"},
    {"id": "pyth", "name": "Pyth Network", "symbol": "PYTH", "chain": "Solana", "coingecko_id": "pyth-network", "logo": "https://assets.coingecko.com/coins/images/31924/large/pyth.png"},
    {"id": "worldcoin", "name": "Worldcoin", "symbol": "WLD", "chain": "Ethereum", "coingecko_id": "worldcoin-wld", "logo": "https://assets.coingecko.com/coins/images/31069/large/worldcoin.jpeg"},
    {"id": "dydx", "name": "dYdX", "symbol": "DYDX", "chain": "Cosmos", "coingecko_id": "dydx", "logo": "https://assets.coingecko.com/coins/images/17500/large/hjnIm9bV.jpg"},
    {"id": "blur", "name": "Blur", "symbol": "BLUR", "chain": "Ethereum", "coingecko_id": "blur", "logo": "https://assets.coingecko.com/coins/images/28453/large/blur.png"},
    {"id": "zksync", "name": "zkSync", "symbol": "ZK", "chain": "Ethereum", "coingecko_id": "zksync", "logo": "https://assets.coingecko.com/coins/images/38043/large/ZKTokenBlack.png"},
    {"id": "layerzero", "name": "LayerZero", "symbol": "ZRO", "chain": "Ethereum", "coingecko_id": "layerzero", "logo": "https://assets.coingecko.com/coins/images/28206/large/ftxG9_TJ_400x400.jpeg"},
    {"id": "hyperliquid", "name": "Hyperliquid", "symbol": "HYPE", "chain": "Hyperliquid", "coingecko_id": "hyperliquid", "logo": "https://assets.coingecko.com/coins/images/36139/large/hyperliquid.png"},
    {"id": "ethena", "name": "Ethena", "symbol": "ENA", "chain": "Ethereum", "coingecko_id": "ethena", "logo": "https://assets.coingecko.com/coins/images/36530/large/ethena.png"},
    {"id": "wormhole", "name": "Wormhole", "symbol": "W", "chain": "Solana", "coingecko_id": "wormhole", "logo": "https://assets.coingecko.com/coins/images/35087/large/womrhole_logo_full_color_rgb_2000px_72ppi_fb766ac85a.png"},
]

STATIC_DATA = {
    "arbitrum":   {"unlock": "92.6M",  "date": "Apr 16, 2026", "supply": "10B",   "percent": "9.3%",  "mcap": "$1.12B",  "description": "Arbitrum is a Layer 2 scaling solution for Ethereum."},
    "optimism":   {"unlock": "24.1M",  "date": "Apr 22, 2026", "supply": "4.2B",  "percent": "5.7%",  "mcap": "$0.44B",  "description": "Optimism is a fast, stable L2 blockchain built on Ethereum."},
    "aptos":      {"unlock": "11.3M",  "date": "May 01, 2026", "supply": "1B",    "percent": "1.1%",  "mcap": "$3.12B",  "description": "Aptos is a Layer 1 blockchain focused on safety and scalability."},
    "sui":        {"unlock": "64.0M",  "date": "May 08, 2026", "supply": "10B",   "percent": "6.4%",  "mcap": "$8.54B",  "description": "Sui is a Layer 1 blockchain designed for high throughput."},
    "avalanche":  {"unlock": "8.5M",   "date": "May 15, 2026", "supply": "720M",  "percent": "1.2%",  "mcap": "$11.2B",  "description": "Avalanche is a fast, low-cost, and eco-friendly blockchain."},
    "solana":     {"unlock": "18.2M",  "date": "May 20, 2026", "supply": "580M",  "percent": "3.1%",  "mcap": "$38.4B",  "description": "Solana is a high-performance blockchain supporting fast transactions."},
    "near":       {"unlock": "22.0M",  "date": "Jun 01, 2026", "supply": "1B",    "percent": "2.2%",  "mcap": "$1.38B",  "description": "NEAR Protocol is a user-friendly blockchain platform."},
    "cosmos":     {"unlock": "12.5M",  "date": "Jun 08, 2026", "supply": "390M",  "percent": "3.2%",  "mcap": "$0.67B",  "description": "Cosmos is an ecosystem of connected blockchains."},
    "chainlink":  {"unlock": "30.0M",  "date": "Jun 15, 2026", "supply": "1B",    "percent": "3.0%",  "mcap": "$8.75B",  "description": "Chainlink is a decentralized oracle network."},
    "uniswap":    {"unlock": "15.0M",  "date": "Jun 20, 2026", "supply": "1B",    "percent": "1.5%",  "mcap": "$3.04B",  "description": "Uniswap is the leading decentralized exchange protocol."},
    "aave":       {"unlock": "5.0M",   "date": "Jun 25, 2026", "supply": "16M",   "percent": "31.2%", "mcap": "$1.51B",  "description": "Aave is a decentralized lending and borrowing protocol."},
    "polygon":    {"unlock": "45.0M",  "date": "May 25, 2026", "supply": "10B",   "percent": "4.5%",  "mcap": "$0.95B",  "description": "Polygon is a Layer 2 scaling solution for Ethereum."},
    "starknet":   {"unlock": "128M",   "date": "Jul 15, 2026", "supply": "10B",   "percent": "1.3%",  "mcap": "$0.33B",  "description": "StarkNet is a ZK-Rollup operating on Ethereum."},
    "celestia":   {"unlock": "75.0M",  "date": "Jul 20, 2026", "supply": "1B",    "percent": "7.5%",  "mcap": "$0.29B",  "description": "Celestia is a modular blockchain focused on data availability."},
    "sei":        {"unlock": "900M",   "date": "Jul 25, 2026", "supply": "10B",   "percent": "9.0%",  "mcap": "$0.55B",  "description": "Sei is the fastest Layer 1 blockchain for trading."},
    "injective":  {"unlock": "6.0M",   "date": "Aug 01, 2026", "supply": "100M",  "percent": "6.0%",  "mcap": "$0.29B",  "description": "Injective is a blockchain built for finance."},
    "pyth":       {"unlock": "2.1B",   "date": "Aug 08, 2026", "supply": "10B",   "percent": "21%",   "mcap": "$0.43B",  "description": "Pyth Network delivers real-time market data."},
    "worldcoin":  {"unlock": "50.0M",  "date": "Aug 15, 2026", "supply": "10B",   "percent": "0.5%",  "mcap": "$0.29B",  "description": "Worldcoin is focused on global identity and financial inclusion."},
    "dydx":       {"unlock": "28.0M",  "date": "Jul 01, 2026", "supply": "1B",    "percent": "2.8%",  "mcap": "$0.09B",  "description": "dYdX is a decentralized perpetuals trading platform."},
    "blur":       {"unlock": "200M",   "date": "Jul 08, 2026", "supply": "3B",    "percent": "6.7%",  "mcap": "$0.02B",  "description": "Blur is an NFT marketplace for professional traders."},
    "zksync":     {"unlock": "700M",   "date": "Jun 16, 2026", "supply": "21B",   "percent": "3.3%",  "mcap": "$0.31B",  "description": "zkSync is a ZK rollup scaling Ethereum."},
    "layerzero":  {"unlock": "85.0M",  "date": "Jun 30, 2026", "supply": "1B",    "percent": "8.5%",  "mcap": "$1.92B",  "description": "LayerZero is an omnichain interoperability protocol."},
    "hyperliquid":{"unlock": "12.0M",  "date": "May 28, 2026", "supply": "1B",    "percent": "1.2%",  "mcap": "$13.8B",  "description": "Hyperliquid is a high-performance decentralized exchange."},
    "ethena":     {"unlock": "300M",   "date": "Jun 05, 2026", "supply": "15B",   "percent": "2.0%",  "mcap": "$0.71B",  "description": "Ethena is a synthetic dollar protocol on Ethereum."},
    "wormhole":   {"unlock": "600M",   "date": "Jun 12, 2026", "supply": "10B",   "percent": "6.0%",  "mcap": "$0.35B",  "description": "Wormhole is a cross-chain messaging protocol."},
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

async def fetch_price_changes(coingecko_ids: list):
    try:
        ids = ",".join(coingecko_ids)
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

@app.get("/")
def root():
    return {"message": "Token Unlock Tracker API", "status": "running", "version": "3.0"}

@app.get("/unlocks")
async def get_unlocks(chain: str = None, search: str = None, sort: str = "date"):
    protocols = PROTOCOLS.copy()
    if chain and chain != "All":
        protocols = [p for p in protocols if p["chain"].lower() == chain.lower()]
    if search:
        protocols = [p for p in protocols if search.lower() in p["name"].lower() or search.lower() in p["symbol"].lower()]

    coingecko_ids = [p["coingecko_id"] for p in protocols]
    prices = await fetch_prices(coingecko_ids)
    changes = await fetch_price_changes(coingecko_ids)

    result = []
    for p in protocols:
        static = STATIC_DATA.get(p["id"], {})
        price_key = f"coingecko:{p['coingecko_id']}"
        price_data = prices.get(price_key, {})
        price = price_data.get("price")
        change_data = changes.get(p["coingecko_id"], {})
        change_24h = change_data.get("usd_24h_change", 0)
        token = {
            **p,
            **static,
            "price": f"${price:.3f}" if price else "N/A",
            "change_24h": round(change_24h, 2) if change_24h else 0,
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
    changes = await fetch_price_changes([protocol["coingecko_id"]])
    price_key = f"coingecko:{protocol['coingecko_id']}"
    price = prices.get(price_key, {}).get("price")
    change_data = changes.get(protocol["coingecko_id"], {})
    change_24h = change_data.get("usd_24h_change", 0)
    return {
        **protocol,
        **static,
        "price": f"${price:.3f}" if price else "N/A",
        "change_24h": round(change_24h, 2) if change_24h else 0,
    }

@app.get("/search")
async def search_tokens(q: str = ""):
    protocols = [p for p in PROTOCOLS if q.lower() in p["name"].lower() or q.lower() in p["symbol"].lower()]
    return {"tokens": protocols, "total": len(protocols)}

@app.get("/chains")
def get_chains():
    chains = list(set(p["chain"] for p in PROTOCOLS))
    return {"chains": sorted(chains)}