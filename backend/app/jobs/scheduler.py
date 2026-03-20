from apscheduler.schedulers.background import BackgroundScheduler
from jobs.ingest import ingest_gold, ingest_stocks

scheduler = BackgroundScheduler()

scheduler.add_job(ingest_gold, "interval", minutes=5)
scheduler.add_job(ingest_stocks, "interval", minutes=5)

def start():
    scheduler.start()