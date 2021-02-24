from urllib.request import urlopen
from pymongo import MongoClient
from pyquery import PyQuery as pq

client = MongoClient('localhost', 27017)

db = client.priceTrackerDb
trackers_collection = db.trackermodels

def runScraperAndSave():
    trackers = trackers_collection.find({})
    for tracker in trackers:
        d = pq(url=tracker['url'], opener=lambda url, **kw: urlopen(tracker['url']).read())
        price = d('.pro-price').text().strip()
        trackers_collection.update_one({'_id': tracker['_id']}, {'$push': {'pricepoints': price}})

