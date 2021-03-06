import schedule, time
from web_scraper import run_scraper_and_save

schedule.every(10).seconds.do(run_scraper_and_save)

while True:
    schedule.run_pending()
    time.sleep(1)