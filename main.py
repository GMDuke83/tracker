from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bitget_api import BitgetAPI
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/positions")
def get_positions():
    bitget = BitgetAPI()
    response = bitget.get_positions()

    # Fehlerbehandlung
    if not isinstance(response, dict) or "data" not in response or not response["data"]:
        return {
            "error": response.get("msg", "API error") if isinstance(response, dict) else "No response",
            "raw": response
        }

    result = []
    for item in response["data"]:
        result.append({
            "symbol": item.get("symbol", "N/A"),
            "exchange": "Bitget",
            "side": item.get("holdSide", "N/A").capitalize(),
            "leverage": float(item.get("leverage", 0)),
            "marginType": item.get("marginMode", "Isolated"),
            "entryPrice": float(item.get("averageOpenPrice", 0)),
            "marketPrice": float(item.get("marketPrice", 0)),
            "liqPrice": float(item.get("liquidationPrice", 0)),
            "pnlUSD": float(item.get("unrealizedPL", 0)),
            "pnlPercent": float(item.get("unrealizedPLRatio", 0)) * 100,
            "openTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        })

    return result
