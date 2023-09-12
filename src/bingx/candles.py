from datetime import datetime, timedelta
import time
import credential
import json
import re

re_default = r'[^a-zA-Z0-9\s]' 
def candles(symbol,interval,limit):
    current_datetime = datetime.now()
    resultant_date = current_datetime - timedelta(days=limit)
    desired_time = datetime(resultant_date.year, resultant_date.month, resultant_date.day, 15, 59, 59)
    start_epoch_timestamp = int(str(int(desired_time.timestamp()))+'000')
    end_epoch_timestamp = int(str(int(time.time()))+'000')
    payload = {}
    path = '/openApi/spot/v1/market/kline'
    method = 'GET'
    paramsMap = {
    'symbol': symbol,
    'interval': interval, #(3m, 5m, 10m  = minute |  1h, 2h, 4h = hour | 1d, 3d, 8d = day | 1w, 2w, 8w = week | 1M, 2M, 6M = month)
    'startTime': start_epoch_timestamp,
    'endTime': end_epoch_timestamp,
    'limit' : limit #qty limit inverval
    }  
    paramsStr = credential.praseParam(paramsMap)
    json_data = json.loads(credential.send_request(method, path, paramsStr, payload))

    if 'data' in json_data:
        return json_data  
    else:
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))
        return error