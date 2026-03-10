import pandas as pd
import numpy as np


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Empty DataFrame received for feature creation")

    required_columns = {"Close", "Volume"}
    if not required_columns.issubset(df.columns):
        raise ValueError("Required columns 'Close' and 'Volume' not found")

    df = df.copy()

    # 1️⃣ Return (MUST be first)
    df["Return"] = df["Close"].pct_change()

    # 2️⃣ Moving Averages
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    # 3️⃣ Volatility (uses Return)
    df["Volatility"] = df["Return"].rolling(window=20).std()

    # 4️⃣ Volume Change
    df["Volume_Change"] = df["Volume"].pct_change()

    # 5️⃣ RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))

    df.dropna(inplace=True)
    return df
