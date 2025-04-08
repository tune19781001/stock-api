from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import ta

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock")
def get_stock_data(symbol: str):
    try:
        # 移動平均・RSI計算のために25日分取得
        data = yf.Ticker(symbol).history(period="30d")

        # 最新の終値と出来高
        latest = data.iloc[-1]
        price = float(latest["Close"])
        volume = int(latest["Volume"])

        # RSI計算
        rsi_series = ta.momentum.RSIIndicator(close=data["Close"]).rsi()
        rsi = round(rsi_series.iloc[-1], 2)

        # 移動平均線（5日・25日）計算
        ma_5 = round(data["Close"].rolling(window=5).mean().iloc[-1], 2)
        ma_25 = round(data["Close"].rolling(window=25).mean().iloc[-1], 2)

        return {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "rsi": rsi,
            "ma_5": ma_5,
            "ma_25": ma_25
        }
    except Exception as e:
        return {"error": str(e)}
