import datetime, os, re, sys
from urllib.request import urlopen
from pymongo import MongoClient
from pyquery import PyQuery as pq
from tracker import Tracker

client = None
mongo_uri = os.environ.get('MONGO_URI')
if mongo_uri:
    client = MongoClient(mongo_uri)
else:
    client = MongoClient('localhost', 27017)

db = client.priceTrackerDb
trackers_collection = db.trackermodels
pricepoints_collection = db.pricepointsmodels

def run_scraper_and_save():
    trackers = get_trackers()

    for _tracker in trackers:
        get_price_and_process_tracker(_tracker)

    sys.exit('Done')     

def get_trackers():        
    trackers = trackers_collection.find({})
    out = []

    for tracker in trackers:
        out.append(Tracker(
            tracker['_id'],
            tracker['url'],
            tracker['watcherId'],
            tracker['currentPrice'],
            tracker['alertPrice'],
            tracker['lowestPrice']))
    
    return out

def get_price_and_process_tracker(tracker):
    updated_urls = set()
    new_price = get_price_for_tracker(tracker)

    db_update = tracker.create_db_object_for_update(new_price)

    update_tracker(tracker, db_update)

    if tracker.url not in updated_urls:
        update_pricepoints(tracker.url, new_price)
        updated_urls.add(tracker.url)

    if tracker.should_alert_user(new_price):
        # send email to user here
        print('should send email to id: ', tracker.watcher_id)


def get_price_for_tracker(tracker):
    d = pq(url=tracker.url, opener=lambda url, **kw: urlopen(tracker.url).read())
    _price = d('.pro-price').text().strip()
    return parse_price(_price)

def update_tracker(tracker, update):
    # Update tracker collection
    trackers_collection.find_one_and_update(
        {'_id': tracker._id},
        update
    )

def update_pricepoints(url, new_price):
    now = datetime.datetime.utcnow()

    # Update pricepoints collection
    pricepoints_collection.update_one(
            {'url': url},
            {
                '$push': {
                    'pricepoints': {
                        'timestamp': now,
                        'price': new_price
                    }
                }
            },
            upsert=True
        )

def parse_price(price):
    pattern = r"[\d.|,]+"
    s = re.search(pattern, price)
    if s:
        return float(s.group().replace('.', '').replace(',', '.'))
    else:
        raise RuntimeError('Could not parse the price: ', price)