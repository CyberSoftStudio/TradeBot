from Predictor import Predictor
import numpy as np
import time

predictor = Predictor([])

INFILE = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\908CDDF6DDEF089609CFD48700109B47\\MQL5\\Files\\input.txt'
OUTFILE = 'C:\\Users\\ASus\\AppData\\Roaming\\MetaQuotes\\Terminal\\908CDDF6DDEF089609CFD48700109B47\\MQL5\\Files\\output.txt'

while True:
    next_time = time.time() + 10
    with open(INFILE, 'rb') as infile:
        lines = infile.readlines()
        try:
            line = lines[-1].decode('utf16')
        except:
            line = "none"

    '''print(line)'''

    if line[:4] == 'data':
        data = np.array([float(x) for x in line[5:].split(' ')])
        shift_window = list(data[-30:])
        shift_window.reverse()

        for i in range(1, len(shift_window)):
            tmp = shift_window[i] - shift_window[0]
            shift_window[i] = shift_window[0] - tmp

        data = list(data[30:])
        data.extend(shift_window)

        predictor.set_data(data)
        interval = predictor.predict()
        response = "none"
        if len(interval) > 0:
            interval['timestamp'] = time.time()
            response = ';'.join([x+'='+str(interval[x]) for x in interval.keys()])
            print('prediction:' + response)
        with open(OUTFILE, 'w') as outfile:
            print('prediction:' + response, file=outfile)
    elif line[:3] == 'set':
        # field1=value1;field2=value2;...
        token = line[4:].split(';')
        new_config = {}
        for x in token:
            key, value = x.split('=')
            try:
                new_config[key] = float(value)
            except:
                new_config[key] = value

        predictor.change_config(new_config)
        print("Done", new_config)

    time_to_sleep = next_time - time.time()
    while time_to_sleep < 0:
        time_to_sleep += 10

    time.sleep(time_to_sleep)





