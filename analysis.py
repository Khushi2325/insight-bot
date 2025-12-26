import yfinance as yf
import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_stock(symbol):
    df = yf.download(symbol, period="1y", interval="1d")

    if df.empty or len(df) < 200:
        return None

    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()
    df["RSI"] = calculate_rsi(df["Close"])

    close_series = df["Close"].squeeze()

    price = float(close_series.iloc[-1])
    ma50 = float(df["MA50"].squeeze().iloc[-1])
    ma200 = float(df["MA200"].squeeze().iloc[-1])
    rsi = float(df["RSI"].squeeze().iloc[-1])

    if price > ma50 and price > ma200:
        structure = "positive"
    elif price < ma50 and price < ma200:
        structure = "negative"
    else:
        structure = "neutral"

    dates = close_series.index[-100:].strftime("%Y-%m-%d").tolist()
    prices = close_series.iloc[-100:].astype(float).tolist()
    ma50_list = df["MA50"].squeeze().iloc[-100:].astype(float).tolist()
    rsi_list = df["RSI"].squeeze().iloc[-100:].astype(float).tolist()

    return {
        "symbol": symbol,
        "price": round(price, 2),
        "structure": structure,
        "rsi": round(rsi, 2),
        "dates": dates,
        "prices": prices,
        "ma50": ma50_list,
        "rsi_series": rsi_list
    }


