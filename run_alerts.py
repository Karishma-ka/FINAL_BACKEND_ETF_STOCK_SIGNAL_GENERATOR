from apscheduler.schedulers.blocking import BlockingScheduler
from app.alerts.alert_engine import check_alerts

scheduler = BlockingScheduler()


def run_alerts():

    ticker = "AAPL"
    threshold_price = 185
    user_email = "user@gmail.com"

    print("Running alert check...")

    check_alerts(ticker, threshold_price, user_email)


scheduler.add_job(run_alerts, "interval", minutes=5)

scheduler.start()