from scripts.Trader_bitmex import Trader_bitmex


exchange_traders ={
    "bitmex": Trader_bitmex
}


class Trader:
    def __init__(self):
        pass

    @staticmethod
    def trader_fabric(self, exchange_name, auth, test = False):
        return exchange_traders[exchange_name](auth, test=test)