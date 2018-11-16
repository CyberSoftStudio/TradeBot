from Predictor import Predictor
import numpy as np
import time
import json
import pandas as pd
import libs.histogramma_lib as hlib
import math

predictor = Predictor([])

INFILE = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\908CDDF6DDEF089609CFD48700109B47\\MQL5\\Files\\input.txt'
OUTFILE = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\908CDDF6DDEF089609CFD48700109B47\\MQL5\\Files\\output.txt'
LOGFILE = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\908CDDF6DDEF089609CFD48700109B47\\MQL5\\Files\\log.txt'
TESTOUT = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\908CDDF6DDEF089609CFD48700109B47\\MQL5\\Files\\output.csv'

INFILE = 'input.txt'
OUTFILE = 'output.txt'
LOGFILE = 'log.txt'
TESTOUT = 'output.csv'

HIST_CONFIG = {
    "pref_prob" : 0.01, # min probability
    "suff_prob" : 0.01  # max probability
}

trend_window_size = 32 # 16 8



while True:
#    next_time = time.time() + 2

    print("Awake")
    try:
        with open(INFILE, 'rb') as infile:
            lines = infile.readlines()
            print(lines[-1].decode('utf16'))
            try:
                req = json.loads(lines[-1].decode('utf16'))
            except Exception as e:
                print(e)
                req = None
    except:
        time.sleep(2)
        continue
    '''print(timef, line)'''
    if(req is None) :
        print("req is none")
        time.sleep(2)
        continue

    try:

        if req['test'] == False:
            close = [float(x) for x in req['data']]
            timef = req['timef']

            # timef = req['timeframe']

            close = np.array(close)

            predictor.set_data(close)
            interval = predictor.predict()

            mina, maxa, trend = hlib.get_bound_by_hist_linear_approx(close[-trend_window_size:], **HIST_CONFIG)

            interval['minmaxamplitude'] = maxa - mina
            interval['mina'] = mina
            interval['maxa'] = maxa
            interval['last_point'] = trend[-1]
            interval['trend'] = math.atan((trend[-1] - trend[0]))
            interval['timef'] = timef

            response = ';'.join([x+'='+str(interval[x]) for x in interval.keys()])

            print('prediction=true;' + response)
            try:
                print("Write prediction to OUTPUT file")
                with open(OUTFILE, 'w') as outfile:
                    print('prediction=true;' + response, file=outfile)
                print("Finished")
            except Exception as e:
                print(e)


            try:
                print("Write prediction to LOG file")
                with open(LOGFILE, 'a+') as logfile:
                    print('prediction=true;' + response, file=logfile)
                print("Finished")
            except Exception as e:
                print(e)
        else:

            print("Start test")
            price_series = np.array([float(x['close']) for x in req['data']])
            #print(price_series)
            time_series = [x['timef'] for x in req['data']]
            #print(time_series)
            window_size = 256
            limit = len(price_series) - window_size
            intervals = []
            for i in range(0, limit):
                print("i == ", i)
                print('{}/{}'.format(i, limit))
                try:
                    window = price_series[i:i + window_size]
                    predictor.set_data(window)
                    window = price_series[i + predictor.config['shift']: i + window_size + predictor.config['shift']]
                    interval = predictor.predict()
                    M = np.zeros((2, 2))
                except Exception as e:
                    print("Exception! Prediction")
                    print(e)
                    print(" ")
                    continue

                print("##############################################################################")

                try:
                    mina, maxa, trend = hlib.get_bound_by_hist_linear_approx(window[-trend_window_size:], **HIST_CONFIG)
                except Exception as e:
                    print("Exception! Histogramma")
                    print(e)
                    print(" ")
                    continue

                interval['minmaxamplitude'] = maxa - mina
                interval['mina'] = mina
                interval['maxa'] = maxa
                interval['last_point'] = trend[-1]
                interval['trend'] = math.atan((trend[-1] - trend[0]))

                if len(interval) > 7:
                    interval['miny'] = int(interval['miny'])
                    interval['maxy'] = int(interval['maxy'])
                    interval['center'] = int(interval['center'])
                    # interval['trend'] = float(interval['trend'])
                    interval['amplitude'] = float(interval['amplitude'])
                    interval['start'] = 225

                    interval['miny'] += i
                    interval['maxy'] += i
                    interval['center'] += i
                    interval['start'] += i


                    print("Interval predicted", interval)

                    intervals.append((interval, M, window, i))

            intervals = sorted(intervals, key=lambda x: (x[0]['miny'], x[0]['center'] - x[0]['miny']))

            resdata = [x[0] for x in intervals]

            intervals_json = {
                'start': [],
                'miny': [],
                'maxy': [],
                'center': [],
                'trend': [],
                'amplitude': [],
                'minmaxamplitude': [],
                'last_point': [],
                'mina': [],
                'maxa': []

            }

            for x in resdata:
                for key, val in x.items():
                    intervals_json[key].append(val)


            csv_data = pd.DataFrame(intervals_json)
            csv_data[['start', 'miny', 'center', 'maxy']] = csv_data[['start', 'miny', 'center', 'maxy']].applymap(
                    lambda x: time_series[min(x + 30, len(time_series) - 1)])
            csv_data.to_csv(TESTOUT, index=None)
            print("Test finish!!!")
            break

    except Exception as e:
        print(e)


#time_to_sleep = next_time - time.time()
 #      time_to_sleep = -time_to_sleep
  #  '''while time_to_sleep < 0:'''
   # '''    time_to_sleep += 1'''
    #if time_to_sleep > 0:
    time.sleep(2)





