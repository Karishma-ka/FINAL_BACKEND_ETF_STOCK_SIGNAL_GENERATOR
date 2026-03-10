import pandas as pd
import numpy as np
from app.services.data_fetch import fetch_stock_data
from app.services.data_clean import clean_data
from app.services.data_features import add_features
from app.services.data_models import load_artifacts


def backtest_strategy(ticker: str):

    model, scaler, features = load_artifacts(ticker)

    df = fetch_stock_data(ticker)
    df = clean_data(df)
    df = add_features(df)

    # Compute returns
    df["Daily_Return"] = df["Close"].pct_change()

    df = df.dropna()

    # Feature selection
    X = df[features]

    # Clean infinite values
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.dropna()

    # Align dataframe
    df = df.loc[X.index]

    # Scale
    X_scaled = scaler.transform(X)

    # Predict
    df["prediction"] = model.predict(X_scaled)

    # Strategy return
    df["strategy_return"] = (
        df["prediction"].shift(1) * df["Daily_Return"]
    ).fillna(0)

    # Cumulative returns
    df["cumulative_market"] = (
        1 + df["Daily_Return"]
    ).cumprod()

    df["cumulative_strategy"] = (
        1 + df["strategy_return"]
    ).cumprod()

    # ==============================
    # 📊 PERFORMANCE ANALYZER
    # ==============================

    # Total returns
    market_return = df["cumulative_market"].iloc[-1] - 1
    strategy_return = df["cumulative_strategy"].iloc[-1] - 1

    # Sharpe Ratio
    sharpe_ratio = np.sqrt(252) * (
        df["strategy_return"].mean() /
        df["strategy_return"].std()
    )

    # Max Drawdown
    rolling_max = df["cumulative_strategy"].cummax()
    drawdown = (
        df["cumulative_strategy"] - rolling_max
    ) / rolling_max
    max_drawdown = drawdown.min()

    # Win Rate
    win_rate = (
        (df["strategy_return"] > 0).sum() /
        len(df["strategy_return"])
    ) * 100

    return {
        "ticker": ticker,
        "market_return_%": round(market_return * 100, 2),
        "strategy_return_%": round(strategy_return * 100, 2),
        "outperformance_%": round(
            (strategy_return - market_return) * 100, 2
        ),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "max_drawdown_%": round(max_drawdown * 100, 2),
        "win_rate_%": round(win_rate, 2)
    }