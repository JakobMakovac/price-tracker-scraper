import time, os
from flask import Flask
from web_scraper import run_scraper_and_save

if os.environ.get('PORT') != None:
    port = os.environ.get('PORT')
else:
    port = '5000'

class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                run_scraper_and_save()
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = MyFlaskApp(__name__)
app.run(port=port)
