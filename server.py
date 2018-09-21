from flask import Flask, jsonify, request
import json
import time
from Bot import Bot

# My scripts import
from libs.prediction_lib import predict, load_cnn
from Predictor import Predictor

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
        timestamp = json.loads(request.data)['timestamp']
        print(window)
        # rects, _, _ = predict(window)
        predictor.set_data(window)
        interval = predictor.predict()
        print(interval)
        result = "{}"
        if len(interval) > 0:
            interval['miny'] = timestamp * (interval['miny'] - 226) * 300
            interval['center'] = timestamp * (interval['center'] - 226) * 300

            result = json.dumps(interval)

        return result

    except Exception as e:
        print(request.args)
        print(e)
        return jsonify({'error': True, 'why':str(e)})


@app.route('/set_configuration', methods=['GET', 'POST'])
def set_configuration():
    config = json.loads(request.data)
    predictor.change_config(config)
    return jsonify({'status':'OK'})


if __name__ == "__main__":
    predictor = Predictor([])


app.run(host='0.0.0.0')