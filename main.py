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
    {"id": "arbitrum", "name": "Arbitrum", "symbol": "ARB", "chain": "Ethereum", "coingecko_id": "arbitrum", "unlock": "92.6M", "date": "Apr 16, 2026", "supply": "10B", "percent": "9.3%", "mcap": "$1.12B", "description": "Arbitrum is a Layer 2 scaling solution for Ethereum."},
    {"id": "optimism", "name": "Optimism", "symbol": "OP", "chain": "Ethereum", "coingecko_id": "optimism", "unlock": "24.1M", "date": "Apr 22, 2026", "supply": "4.2B", "percent": "5.7%", "mcap": "$0.44B", "description": "Optimism is a fast, stable L2 blockchain built on Ethereum."},
    {"id": "aptos", "name": "Aptos", "symbol": "APT", "chain": "Aptos", "coingecko_id": "aptos", "unlock": "11.3M", "date": "May 01, 2026", "supply": "1B", "percent": "1.1%", "mcap": "$3.12B", "description": "Aptos is a Layer 1 blockchain focused on safety and scalability."},
    {"id": "sui", "name": "Sui", "symbol": "SUI", "chain": "Sui", "coingecko_id": "sui", "unlock": "64.0M", "date": "May 08, 2026", "supply": "10B", "percent": "6.4%", "mcap": "$8.54B", "description": "Sui is a Layer 1 blockchain designed for high throughput."},
    {"id": "avalanche", "name": "Avalanche", "symbol": "AVAX", "chain": "Avalanche", "coingecko_id": "avalanche-2", "unlock": "8.5M", "date": "May 15, 2026", "supply": "720M", "percent": "1.2%", "mcap": "$11.2B", "description": "Avalanche is a fast, low-cost, and eco-friendly blockchain."},
    {"id": "solana", "name": "Solana", "symbol": "SOL", "chain": "Solana", "coingecko_id": "solana", "unlock": "18.2M", "date": "May 20, 2026", "supply": "580M", "percent": "3.1%", "mcap": "$38.4B", "description": "Solana is a high-performance blockchain supporting fast transactions."},
    {"id": "near", "name": "Near", "symbol": "NEAR", "chain": "Near", "coingecko_id": "near", "unlock": "22.0M", "date": "Jun 01, 2026", "supply": "1B", "percent": "2.2%", "mcap": "$1.38B", "description": "NEAR Protocol is a user-friendly blockchain platform."},
    {"id": "cosmos", "name": "Cosmos", "symbol": "ATOM", "chain": "Cosmos", "coingecko_id": "cosmos", "unlock": "12.5M", "date": "Jun 08, 2026", "supply": "390M", "percent": "3.2%", "mcap": "$0.67B", "description": "Cosmos is an ecosystem of connected blockchains."},
    {"id": "chainlink", "name": "Chainlink", "symbol": "LINK", "chain": "Ethereum", "coingecko_id": "chainlink", "unlock": "30.0M", "date": "Jun 15, 2026", "supply": "1B", "percent": "3.0%", "mcap": "$8.75B", "description": "Chainlink is a decentralized oracle network."},
    {"id": "uniswap", "name": "Uniswap", "symbol": "UNI", "chain": "Ethereum", "coingecko_id": "uniswap", "unlock": "15.0M", "date": "Jun 20, 2026", "supply": "1B", "percent": "1.5%", "mcap": "$3.04B", "description": "Uniswap is the leading decentralized exchange protocol."},
    {"id": "aave", "name": "Aave", "symbol": "AAVE", "chain": "Ethereum", "coingecko_id": "aave", "unlock": "5.0M", "date": "Jun 25, 2026", "supply": "16M", "percent": "31.2%", "mcap": "$1.51B", "description": "Aave is a decentralized lending and borrowing protocol."},
    {"id": "polygon", "name": "Polygon", "symbol": "MATIC", "chain": "Ethereum", "coingecko_id": "matic-network", "unlock": "45.0M", "date": "May 25, 2026", "supply": "10B", "percent": "4.5%", "mcap": "$0.95B", "description": "Polygon is a Layer 2 scaling solution for Ethereum."},
    {"id": "starknet", "name": "Starknet", "symbol": "STRK", "chain": "Ethereum", "coingecko_id": "starknet", "unlock": "128M", "date": "Jul 15, 2026", "supply": "10B", "percent": "1.3%", "mcap": "$0.33B", "description": "StarkNet is a ZK-Rollup operating on Ethereum."},
    {"id": "celestia", "name": "Celestia", "symbol": "TIA", "chain": "Celestia", "coingecko_id": "celestia", "unlock": "75.0M", "date": "Jul 20, 2026", "supply": "1B", "percent": "7.5%", "mcap": "$0.29B", "description": "Celestia is a modular blockchain focused on data availability."},
    {"id": "sei", "name": "Sei", "symbol": "SEI", "chain": "Sei", "coingecko_id": "sei-network", "unlock": "900M", "date": "Jul 25, 2026", "supply": "10B", "percent": "9.0%", "mcap": "$0.55B", "description": "Sei is the fastest Layer 1 blockchain for trading."},
    {"id": "injective", "name": "Injective", "symbol": "INJ", "chain": "Cosmos", "coingecko_id": "injective-protocol", "unlock": "6.0M", "date": "Aug 01, 2026", "supply": "100M", "percent": "6.0%", "mcap": "$0.29B", "description": "Injective is a blockchain built for finance."},
    {"id": "pyth", "name": "Pyth Network", "symbol": "PYTH", "chain": "Solana", "coingecko_id": "pyth-network", "unlock": "2.1B", "date": "Aug 08, 2026", "supply": "10B", "percent": "21%", "mcap": "$0.43B", "description": "Pyth Network delivers real-time market data."},
    {"id": "worldcoin", "name": "Worldcoin", "symbol": "WLD", "chain": "Ethereum", "coingecko_id": "worldcoin-wld", "unlock": "50.0M", "date": "Aug 15, 2026", "supply": "10B", "percent": "0.5%", "mcap": "$0.29B", "description": "Worldcoin is focused on global identity and financial inclusion."},
    {"id": "dydx", "name": "dYdX", "symbol": "DYDX", "chain": "Cosmos", "coingecko_id": "dydx", "unlock": "28.0M", "date": "Jul 01, 2026", "supply": "1B", "percent": "2.8%", "mcap": "$0.09B", "description": "dYdX is a decentralized perpetuals trading platform."},
    {"id": "blur", "name": "Blur", "symbol": "BLUR", "chain": "Ethereum", "coingecko_id": "blur", "unlock": "200M", "date": "Jul 08, 2026", "supply": "3B", "percent": "6.7%", "mcap": "$0.02B", "description": "Blur is an NFT marketplace for professional traders."},
    {"id": "zksync", "name": "zkSync", "symbol": "ZK", "chain": "Ethereum", "coingecko_id": "zksync", "unlock": "700M", "date": "Jun 16, 2026", "supply": "21B", "percent": "3.3%", "mcap": "$0.31B", "description": "zkSync is a ZK rollup scaling Ethereum."},
    {"id": "layerzero", "name": "LayerZero", "symbol": "ZRO", "chain": "Ethereum", "coingecko_id": "layerzero", "unlock": "85.0M", "date": "Jun 30, 2026", "supply": "1B", "percent": "8.5%", "mcap": "$1.92B", "description": "LayerZero is an omnichain interoperability protocol."},
    {"id": "hyperliquid", "name": "Hyperliquid", "symbol": "HYPE", "chain": "Hyperliquid", "coingecko_id": "hyperliquid", "unlock": "12.0M", "date": "May 28, 2026", "supply": "1B", "percent": "1.2%", "mcap": "$13.8B", "description": "Hyperliquid is a high-performance decentralized exchange."},
    {"id": "ethena", "name": "Ethena", "symbol": "ENA", "chain": "Ethereum", "coingecko_id": "ethena", "unlock": "300M", "date": "Jun 05, 2026", "supply": "15B", "percent": "2.0%", "mcap": "$0.71B", "description": "Ethena is a synthetic dollar protocol on Ethereum."},
    {"id": "wormhole", "name": "Wormhole", "symbol": "W", "chain": "Solana", "coingecko_id": "wormhole", "unlock": "600M", "date": "Jun 12, 2026", "supply": "10B", "percent": "6.0%", "mcap": "$0.35B", "description": "Wormhole is a cross-chain messaging protocol."},
    {"id": "eigenlayer", "name": "EigenLayer", "symbol": "EIGEN", "chain": "Ethereum", "coingecko_id": "eigenlayer", "unlock": "45.0M", "date": "May 10, 2026", "supply": "1.67B", "percent": "2.7%", "mcap": "$0.45B", "description": "EigenLayer is a restaking protocol on Ethereum."},
    {"id": "jupiter", "name": "Jupiter", "symbol": "JUP", "chain": "Solana", "coingecko_id": "jupiter-exchange-solana", "unlock": "500M", "date": "May 18, 2026", "supply": "13.5B", "percent": "3.7%", "mcap": "$0.89B", "description": "Jupiter is the key liquidity aggregator for Solana."},
    {"id": "jito", "name": "Jito", "symbol": "JTO", "chain": "Solana", "coingecko_id": "jito-governance-token", "unlock": "80.0M", "date": "Jun 03, 2026", "supply": "1B", "percent": "8.0%", "mcap": "$0.21B", "description": "Jito is a liquid staking protocol on Solana."},
    {"id": "pendle", "name": "Pendle", "symbol": "PENDLE", "chain": "Ethereum", "coingecko_id": "pendle", "unlock": "10.0M", "date": "Jun 10, 2026", "supply": "281M", "percent": "3.6%", "mcap": "$0.15B", "description": "Pendle is a yield trading protocol."},
    {"id": "mantle", "name": "Mantle", "symbol": "MNT", "chain": "Ethereum", "coingecko_id": "mantle", "unlock": "150M", "date": "Jun 18, 2026", "supply": "6.2B", "percent": "2.4%", "mcap": "$0.62B", "description": "Mantle is an Ethereum Layer 2 network."},
    {"id": "scroll", "name": "Scroll", "symbol": "SCR", "chain": "Ethereum", "coingecko_id": "scroll-token", "unlock": "40.0M", "date": "Jun 25, 2026", "supply": "1B", "percent": "4.0%", "mcap": "$0.08B", "description": "Scroll is a ZK-EVM Layer 2 on Ethereum."},
    {"id": "movement", "name": "Movement", "symbol": "MOVE", "chain": "Ethereum", "coingecko_id": "movement", "unlock": "200M", "date": "Jul 05, 2026", "supply": "10B", "percent": "2.0%", "mcap": "$0.32B", "description": "Movement is a Move-based blockchain network."},
    {"id": "berachain", "name": "Berachain", "symbol": "BERA", "chain": "Berachain", "coingecko_id": "berachain-bera", "unlock": "25.0M", "date": "Jul 10, 2026", "supply": "500M", "percent": "5.0%", "mcap": "$0.18B", "description": "Berachain is a high-performance EVM blockchain."},
    {"id": "altlayer", "name": "AltLayer", "symbol": "ALT", "chain": "Ethereum", "coingecko_id": "altlayer", "unlock": "180M", "date": "Jul 18, 2026", "supply": "10B", "percent": "1.8%", "mcap": "$0.07B", "description": "AltLayer is a decentralized rollups-as-a-service protocol."},
    {"id": "omni", "name": "Omni Network", "symbol": "OMNI", "chain": "Ethereum", "coingecko_id": "omni-network", "unlock": "12.0M", "date": "Jul 22, 2026", "supply": "100M", "percent": "12.0%", "mcap": "$0.06B", "description": "Omni is a blockchain connecting all Ethereum rollups."},
    {"id": "taiko", "name": "Taiko", "symbol": "TAIKO", "chain": "Ethereum", "coingecko_id": "taiko", "unlock": "50.0M", "date": "Aug 05, 2026", "supply": "1B", "percent": "5.0%", "mcap": "$0.05B", "description": "Taiko is a based rollup on Ethereum."},
]

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
    return {"message": "Token Unlock Tracker API", "status": "running", "version": "5.0"}

@app.get("/unlocks")
async def get_unlocks(chain: str = None, search: str = None):
    tokens = TOKENS.copy()
    if chain and chain != "All":
        tokens = [t for t in tokens if t["chain"].lower() == chain.lower()]
    if search:
        tokens = [t for t in tokens if search.lower() in t["name"].lower() or search.lower() in t["symbol"].lower()]

    coingecko_ids = [t["coingecko_id"] for t in tokens]
    prices = await fetch_prices(coingecko_ids)
    changes = await fetch_price_changes(coingecko_ids)

    result = []
    for token in tokens:
        cid = token["coingecko_id"]
        price_key = f"coingecko:{cid}"
        price = prices.get(price_key, {}).get("price")
        change_data = changes.get(cid, {})
        change_24h = change_data.get("usd_24h_change", 0)
        unlock_num = parse_unlock_amount(token["unlock"])
        unlock_usd = format_usd(unlock_num * price) if price else "N/A"

        result.append({
            **token,
            "price": f"${price:.3f}" if price else "N/A",
            "change_24h": round(change_24h, 2) if change_24h else 0,
            "unlock_usd": unlock_usd,
        })

    return {"tokens": result, "total": len(result)}

@app.get("/unlocks/{token_id}")
async def get_token(token_id: str):
    token = next((t for t in TOKENS if t["id"] == token_id), None)
    if not token:
        return {"error": "Token not found"}
    prices = await fetch_prices([token["coingecko_id"]])
    changes = await fetch_price_changes([token["coingecko_id"]])
    price_key = f"coingecko:{token['coingecko_id']}"
    price = prices.get(price_key, {}).get("price")
    change_24h = changes.get(token["coingecko_id"], {}).get("usd_24h_change", 0)
    unlock_num = parse_unlock_amount(token["unlock"])
    unlock_usd = format_usd(unlock_num * price) if price else "N/A"
    return {
        **token,
        "price": f"${price:.3f}" if price else "N/A",
        "change_24h": round(change_24h, 2) if change_24h else 0,
        "unlock_usd": unlock_usd,
    }

@app.get("/search")
async def search_tokens(q: str = ""):
    tokens = [t for t in TOKENS if q.lower() in t["name"].lower() or q.lower() in t["symbol"].lower()]
    return {"tokens": tokens, "total": len(tokens)}

@app.get("/chains")
def get_chains():
    chains = list(set(t["chain"] for t in TOKENS))
    return {"chains": sorted(chains)}