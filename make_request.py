import requests
import numpy as np
import math
import sys
import json
print(sys.getdefaultencoding())

signal = np.sin(np.linspace(0, 3 * math.pi, 256))

r = requests.get('http://0.0.0.0:5000/prediction', data=json.dumps({'window':list(signal), 'timestamp':0}))
print(r.text)

r = requests.post('http://0.0.0.0:5000/set_configuration', data=json.dumps({'assurance': 0.9}))
print(r.status_code, r.text)
