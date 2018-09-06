from Predictor import Predictor
from TradingSystem import TradingSystem


class Bot:
    def __init__(self, auth_info, test=False, exchange_name = None):
        self.data = []
        self.predictor = Predictor()
        self.trade_system = TradingSystem(auth_info=auth_info, test=test)

    def loop(self):
        pass




