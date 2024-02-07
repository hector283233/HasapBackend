from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import product_amount_count



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(product_amount_count, 'interval', minutes=120)
    scheduler.start()