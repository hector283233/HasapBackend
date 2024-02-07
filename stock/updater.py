from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import schedule_test



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_test, 'interval', hours=1)
    scheduler.start()