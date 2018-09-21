import json
import datetime


class Monitor_bitmex:
    def __init__(self, client):
        self.client = client

    def get_candles(self, count, symbol='xbt'):
        config = {
            'binSize': '5m',
            'partial': True,
            'symbol': symbol,
            'count': count,
            'reverse': True
        }
        return self.client.Trade.Trade_getBucketed(**config).result(2)

    def get_quote(self, symbol, startTime, endTime=None, reverse=False, count=50):
        if endTime is None:
            endTime = datetime.datetime.utcnow()

        return self.client.Quote.Quote_get(symbol=symbol, startTime=startTime, endTime=endTime, reverse=reverse, count=count).result()

    def get_orderbook(self, symbol, count = 50):
        return self.client.OrderBook.OrderBook_getL2(symbol=symbol, depth=count).result(2)

    def get_instrument(self):
        pass

    def get_position(self):
        pass

    def get_balances(self):
        return self.client.User.User_getWallet().result(2)