# import MonitorFabric
# import TraderFabric
# import Monitor
# import Trader
import bitmex
from Monitor_bitmex import Monitor_bitmex
from Trader_bitmex import Trader_bitmex


# пока что только под bitmex, потом сделаю полиморфно
class TradingSystem:
    def __init__(self, auth_info, test=False):
        self.client = bitmex.bitmex(api_key=auth_info['api_public_key'], api_secret=auth_info['api_secret_key'], test=test)
        self.monitor = Monitor_bitmex(self.client)
        self.trader = Trader_bitmex(self.client)

