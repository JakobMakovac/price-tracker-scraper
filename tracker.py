class Tracker:
    def __init__(self, _id, url, watcher_id, curr_price, alert_price, lowest_price):
        self._id = _id
        self.url = url
        self.watcher_id = watcher_id
        self.curr_price = curr_price
        self.alert_price = alert_price
        self.lowest_price = lowest_price

    def should_alert_user(self, price):
        return price <= self.alert_price

    def has_price_changed(self, new_price):
        return new_price != self.curr_price

    def create_db_object_for_update(self, new_price):
        update_object = {}

        if new_price < self.lowest_price:
            update_object['lowestPrice'] = new_price
            update_object['currentPrice'] = new_price
        else:
            update_object['currentPrice'] = new_price

        return {'$set': update_object}