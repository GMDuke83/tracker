from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    return [
        {
            "symbol": "BTC/USDT",
            "exchange": "Bitget",
            "side": "Long",
            "leverage": 5,
            "marginType": "Isolated",
            "entryPrice": 103366.9,
            "marketPrice": 103656.3,
            "liqPrice": 83067.3,
            "pnlUSD": 0.23,
            "pnlPercent": 1.4,
            "openTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        }
    ]