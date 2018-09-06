import bitmex

class Trader_bitmex:
    def __init__(self, auth_info, test=False):
        self.client = bitmex.bitmex(api_key=auth_info['api_public_key'], api_secret=auth_info['api_secret_key'], test=test)

    def make_order(self, orders):
        result = []
        for order in orders:
            result.append(self.client.Order.Order_new(symbol=order.symbol, orderQty = order.quantity, price = order.price).result())

    def cancel_order(self, order_id):
        self.client.Order.Order_cancel(orderID=order_id).result()

    def cancel_all(self):
        self.client.Order.Order_cancelAll().result()

    def amend_order(self, order_id, new_order):
        self.client.Order.Order_amend(orderID=order_id, price=new_order.price)