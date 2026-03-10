import numpy as np
from app.services.data_fetch import fetch_stock_data
from app.services.data_clean import clean_data
from app.services.data_features import add_features
from app.services.data_models import load_artifacts
from app.alerts.email_service import send_email_alert


def check_alerts(ticker: str, threshold_price: float, user_email: str):

    try:

        model, scaler, features = load_artifacts(ticker)

        df = fetch_stock_data(ticker)
        df = clean_data(df)
        df = add_features(df)

        if df.empty:
            print("No data available")
            return

        latest_price = df["Close"].iloc[-1]

        # PRICE ALERT
        if latest_price >= threshold_price:

            message = f"""
PRICE ALERT

Ticker: {ticker}
Current Price: {latest_price}
Threshold: {threshold_price}
"""

            send_email_alert(
                subject=f"{ticker} Price Alert",
                message=message,
                to_email=user_email
            )

        # MODEL ALERT
        X = df[features]

        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.dropna()

        df = df.loc[X.index]

        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)[-1]

        if prediction == 1:

            message = f"""
BUY SIGNAL

Ticker: {ticker}
Current Price: {latest_price}
"""

            send_email_alert(
                subject=f"{ticker} BUY SIGNAL",
                message=message,
                to_email=user_email
            )

    except Exception as e:
        print(f"Alert engine error: {e}")