from Predictor import Predictor
import numpy as np
import time
import json
import pandas as pd

predictor = Predictor([])

INFILE = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\CE014884047B38E535332C971089AB90\\MQL4\\Files\\input.txt'
OUTFILE = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\CE014884047B38E535332C971089AB90\\MQL4\\Files\\output.txt'
LOGFILE = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\CE014884047B38E535332C971089AB90\\MQL4\\Files\\log.txt'

INFILE = 'input.txt'
OUTFILE = 'output.txt'
LOGFILE = 'log.txt'



while True:
#    next_time = time.time() + 2


    try:
        with open(INFILE, 'rb') as infile:
            lines = infile.readlines()

            try:
                req = json.loads(lines[-1].decode('utf16'))
            except:
                req = None
    except:
        time.sleep(2)
        continue
    '''print(timef, line)'''

    try:

        if req['test'] == False:
            close = [float(x) for x in req['data']]
            timef = req['timef']

            # timef = req['timeframe']

            close = np.array(close)

            predictor.set_data(close)
            interval = predictor.predict()
            response = "none"

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

            price_series = np.array([float(x['close']) for x in req['data']])
            # print(price_series)
            time_series = [x['timef'] for x in req['data']]
            window_size = 256
            limit = len(price_series) - window_size
            intervals = []
            for i in range(0, limit):
                print("i == ", i)
                print('{}/{}'.format(i, limit))
                try:
                    predictor.set_data(price_series[i:i + window_size])
                    window = price_series[i + predictor.config['shift']: i + window_size + predictor.config['shift']]
                    interval = predictor.predict()
                    M = np.zeros((2, 2))
                except:
                    break
                print("##############################################################################")
                if len(interval) > 0:
                    interval['miny'] = int(interval['miny'])
                    interval['maxy'] = int(interval['maxy'])
                    interval['center'] = int(interval['center'])
                    interval['trend'] = float(interval['trend'])
                    interval['amplitude'] = float(interval['amplitude'])
                    interval['start'] = 225

                    interval['miny'] += i
                    interval['maxy'] += i
                    interval['center'] += i
                    interval['start'] += i

                    # interval['miny'] = init_time + interval['miny'] * delta_time
                    # interval['maxy'] = init_time + interval['maxy'] * delta_time
                    # interval['center'] = init_time + interval['center'] * delta_time

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
                    'amplitude': []
                }

                for x in resdata:

                    for key, val in x.items():
                        intervals_json[key].append(val)

                csv_data = pd.DataFrame(intervals_json)
                csv_data[['start', 'miny', 'center', 'maxy']] = csv_data[['start', 'miny', 'center', 'maxy']].applymap(
                    lambda x: time_series[min(x, len(time_series) - 1)])
                csv_data.to_csv('output.csv', index=None)

    except Exception as e:
        print(e)

#time_to_sleep = next_time - time.time()
 #      time_to_sleep = -time_to_sleep
  #  '''while time_to_sleep < 0:'''
   # '''    time_to_sleep += 1'''
    #if time_to_sleep > 0:
    time.sleep(2)





