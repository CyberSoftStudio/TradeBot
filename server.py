from flask import Flask, jsonify, request
import json
import time
from Bot import Bot

# My scripts import
from libs.prediction_lib import predict, load_cnn

app = Flask(__name__)


mult_const = 4
window_size = 256 * mult_const
shift = 30 * mult_const
scale = 50 * mult_const
wdname='db6'
wcname='gaus8'
extract_alpha = 0.5


@app.route('/prediction', methods=['GET', 'POST'])
def make_prediction():
    try:
        print(request.data)
        window = json.loads(request.data)['window']
        print(window)
        # rects, _, _ = predict(window)
        correct_rects, segmentations, M = predict(
            window,
            scale=scale,
            assurance=0.5,
            wdname=wdname,
            wcname=wcname,
            shift=shift,
            extract_alpha=extract_alpha,
            key=1,
            mult_const=mult_const
        )

        result = [rect.get_parameters() for rect in correct_rects]
        print(result)
        return jsonify(result)

    except Exception as e:
        print(request.args)
        print(e)
        return jsonify({'error': True, 'why':str(e)})


if __name__ == "__main__":
    bot = Bot()
    bot.trading_loop()
    bot.prediction_loop()
    time.sleep(10)

app.run(host='0.0.0.0')