from Bot import Bot
import time


auth_info = {
    'api_public': 'M9C8G0sR_xyAH-P-McPtGtFU',
    'api_secret': 'virblf2ij2unSG8VNuwsq5VTw0axnIVYwodKlgeAO0wGqVBS'
}

bot = Bot(auth_info, test=False)

while True:
    bot.trading_loop()
    bot.prediction_loop()
    time.sleep(10)