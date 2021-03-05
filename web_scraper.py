import datetime
from urllib.request import urlopen
from pymongo import MongoClient
from pyquery import PyQuery as pq

client = MongoClient('localhost', 27017)

db = client.priceTrackerDb
trackers_collection = db.trackermodels
pricepoints_collection = db.pricepointsmodels

def runScraperAndSave():
    urls = getUniqueUrls()

    for _url in urls:
        now = datetime.datetime.utcnow()
        d = pq(url=_url, opener=lambda url, **kw: urlopen(_url).read())
        _price = d('.pro-price').text().strip()
        pricepoints_collection.update_one(
            {'url': _url},
            {
                '$push': {
                    'pricepoints': {
                        'timestamp': now,
                        'price': _price
                    }
                }
            },
            upsert=True
        )
        

def getUniqueUrls():        
    trackers = trackers_collection.find({})
    urls = set()
    for tracker in trackers:
        urls.add(tracker['url'])
    
    return list(urls)
