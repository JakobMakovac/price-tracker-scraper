import schedule
import time
from web_scraper import runScraperAndSave

schedule.every(10).seconds.do(runScraperAndSave)

while True:
    schedule.run_pending()
    time.sleep(1)