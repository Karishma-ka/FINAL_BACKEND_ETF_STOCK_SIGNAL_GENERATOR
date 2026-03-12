from apscheduler.schedulers.blocking import BlockingScheduler
from app.alerts.alert_engine import check_alerts
import os
scheduler = BlockingScheduler()

# Watchlist of stocks (10 models)
WATCHLIST = [
    "AAPL",
    "MSFT",
    "TSLA",
    "GOOGL",
    "AMZN",
    "NVDA",
    "META",
    "NFLX",
    "AMD",
    "INTC"
]

# Threshold prices
THRESHOLDS = {
    "AAPL": 185,
    "MSFT": 420,
    "TSLA": 250,
    "GOOGL": 160,
    "AMZN": 180,
    "NVDA": 900,
    "META": 500,
    "NFLX": 650,
    "AMD": 190,
    "INTC": 45
}

EMAIL = os.getenv("EMAIL_USER")


def run_alerts():

    print("Running alert check...")

    for ticker in WATCHLIST:

        try:

            threshold_price = THRESHOLDS.get(ticker, 0)

            check_alerts(
                ticker=ticker,
                threshold_price=threshold_price,
                user_email=EMAIL
            )

        except Exception as e:

            print(f"Alert failed for {ticker}: {e}")


# Run every 5 minutes
scheduler.add_job(run_alerts, "interval", minutes=5)

print("Alert scheduler started...")

scheduler.start()
