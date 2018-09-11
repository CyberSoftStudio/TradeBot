from Bot import Bot


auth_info = {
    'api_public': 'M9C8G0sR_xyAH-P-McPtGtFU',
    'api_secret': 'virblf2ij2unSG8VNuwsq5VTw0axnIVYwodKlgeAO0wGqVBS'
}

bot = Bot(auth_info, test=True)

for i in range(700 - 256):
    bot.prediction_loop()
    bot.trading_loop()
    print(bot.trade_system.get_balances())