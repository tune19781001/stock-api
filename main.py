# これは「VSCode」や「Google Colab（ローカルランタイム）」で実行してね！

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import ta

app = FastAPI()

# CORS（GPTからも叩けるように）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock")
def get_stock_data(symbol: str):
    try:
        # 過去14日分のデータを取得（RSI計算用）
        data = yf.Ticker(symbol).history(period="14d")

        # 最新の終値と出来高
        latest = data.iloc[-1]
        price = float(latest["Close"])
        volume = int(latest["Volume"])

        # RSI計算
        rsi_series = ta.momentum.RSIIndicator(close=data["Close"]).rsi()
        rsi = round(rsi_series.iloc[-1], 2)

        return {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "rsi": rsi
        }
    except Exception as e:
        return {"error": str(e)}
