from Bot import Bot
import matplotlib.pyplot as plt

auth_info = {
    'api_public': 'M9C8G0sR_xyAH-P-McPtGtFU',
    'api_secret': 'virblf2ij2unSG8VNuwsq5VTw0axnIVYwodKlgeAO0wGqVBS'
}

bot = Bot(auth_info, test=True)

for i in range(1700 - 256):
    bot.prediction_loop()
    bot.trading_loop()
    bot.trade_system.closeDay()
    print(bot.trade_system.get_balances())

bot.normalize_stats()
print("Stats", bot.get_stats())