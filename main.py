import time, os
from flask import Flask
from web_scraper import run_scraper_and_save

app = Flask(__name__)
app.run(os.environ.get('PORT'))

run_scraper_and_save()
