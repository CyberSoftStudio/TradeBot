import json
import datetime


class Monitor_bitmex:
    def __init__(self, client):
        self.client = client

    def get_quote(self, symbol, startTime, endTime=None, reverse=False, count=50):
        if endTime is None:
            endTime = datetime.datetime.utcnow()

        return self.client.Quote.Quote_get(symbol=symbol, startTime=startTime, endTime=endTime, reverse=reverse, count=count).result()

    def get_instrument(self):
        pass

    def get_position(self):
        pass