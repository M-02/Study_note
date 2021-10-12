import json
import time
import random
import warnings
import requests

import core.config

warnings.filterwarnings('ignore') # Disable SSL related warnings

def requester(url, data, headers, GET, delay):
    if core.config.globalVariables['jsonData']:
        data = json.dumps(data)
    time.sleep(delay)
    user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991']
    if headers:
    	if 'User-Agent' not in headers:
    		headers['User-Agent'] = random.choice(user_agents)
    if GET:
        response = requests.get(url, params=data, headers=headers, verify=False)
    elif core.config.globalVariables['jsonData']:
        response = requests.post(url, json=data, headers=headers, verify=False)
    else:
        response = requests.post(url, data=data, headers=headers, verify=False)
    return response
