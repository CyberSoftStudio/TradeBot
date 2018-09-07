from Bot import Bot
import time

auth_info = {}

bot = Bot(auth_info, test=False)

while True:
    bot.trading_loop()
    bot.prediction_loop()
    time.sleep(10)
