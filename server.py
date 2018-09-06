from flask import Flask, jsonify, request
import json

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
    model_json_path = '../models/model_cwt_10k.json'  # model_nclasses_46_1
    model_h5_path = '../models/model_cwt_10k.h5'
    load_cnn(model_json_path, model_h5_path)

app.run(host='0.0.0.0')