import libs.prediction_lib as plib
import libs.extremumlib as elib
import math
import numpy as np
import json
import matplotlib.pyplot as plt


class Predictor:
    def __init__(self, data):
        self.data = np.array(data)
        self.config = {
            'mult_const': 1,
            'window_size': 256,
            'assurance':0.6,
            'shift': 30,
            'scale': 50,
            'wdname': 'db6',
            'wcname': 'gaus8',
            'extract_alpha': 0.5,
            'model_key': 2,
            'model_json_path': './models/model_cwt_10k.json',  # model_nclasses_46_1
            'model_h5_path': './models/model_cwt_10k.h5'
        }

        plib.load_cnn(self.config['model_json_path'], self.config['model_h5_path'])

    def set_data(self, data):
        self.data = data.copy()

    def request_data(self):
        pass

    @staticmethod
    def _merge_config(config, new_config):
        result_config = {key: value for key, value in config.items()}

        for key in new_config.keys():
            if key in config:
                result_config[key] = new_config[key]

        return result_config

    def _set_init_config(self):
        self.config = {
            'mult_const': 1,
            'window_size': 256,
            'assurance': 0.6,
            'shift': 30,
            'scale': 50,
            'wdname': 'db6',
            'wcname': 'gaus8',
            'extract_alpha': 0.5,
            'model_key': 2,
            'model_json_path': '../models/model_cwt_10k.json',  # model_nclasses_46_1
            'model_h5_path': '../models/model_cwt_10k.h5'
        }

    def change_config(self, new_config):
        self.config = self._merge_config(self.config, new_config)

    def load_config(self, config_json_file):
        new_config = json.load(open(config_json_file))
        self.config = self._merge_config(self.config, new_config)

    @staticmethod
    def get_trend_1(trend):
        return math.atan((trend[-1] - trend[-30])/30)

    @staticmethod
    def get_trend_2(trend):
        return math.atan(trend[-1] - trend[-2])

    @staticmethod
    def get_trend_3(trend):
        res = [math.atan(trend[-1] - trend[-i]) for i in range(2, 11)]
        res = sorted(res)
        return res[len(res)//2 + 1]

    def predict(self, get_trend = None):

        if get_trend is None:
            get_trend = self.get_trend_1

        mult_const      = self.config['mult_const']
        window_size     = self.config['window_size']
        shift           = self.config['shift']
        scale           = self.config['scale']
        wdname          = self.config['wdname']
        wcname          = self.config['wcname']
        extract_alpha   = self.config['extract_alpha']
        assurance       = self.config['assurance']
        key             = self.config['model_key']

        trend = elib.get_trend(self.data)
        window = self.data[-window_size:]
        correct_rects, segmentations, (M, linear_coef) = plib.predict(
            window,
            scale=scale,
            assurance=assurance,
            wdname=wdname,
            wcname=wcname,
            shift=shift,
            extract_alpha=extract_alpha,
            key=key,
            mult_const=mult_const
        )

        if len(segmentations):
            try:
                interval = plib.predict_interval(segmentations[0].segmentation)

                x, y = correct_rects[0].x * mult_const

                interval['maxy'] *= mult_const
                interval['miny'] *= mult_const
                interval['center'] *= mult_const
                interval['amplitude'] *= linear_coef
                interval['trend'] = get_trend(trend)

                print("Interval trend", interval['trend'])

                interval['maxy'] += y
                interval['miny'] += y
                interval['center'] += y
                interval['miny'] = max(226, interval['miny'])

                assert(interval['center'] > interval['miny'])
                return interval
            except Exception as err:
                # print(err)
                # x, y = correct_rects[0].x * mult_const
                # plt.matshow(elib.bound_filter(elib.linear(M[x:x+32, y:y+32]), alpha=self.config['extract_alpha']))
                # plt.matshow(M)
                # plt.show()
                print("Can't predict interval")
                return {}

        return {}

    # def process(self):




