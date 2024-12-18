from datetime import datetime, timedelta
import numpy as np
import time
import credential
import json
import re

re_default = r'[^a-zA-Z0-9\s]' 

'''
This function will return a JSON with Candlestick chart data including 
pen time, max price, min price, close price, filled price, candlestick 
chart close time, and volume
'''
def candles(symbol,interval,limit):
    """
    Retrieve historical candlestick (kline) data for a given trading pair.

    Parameters:
    - symbol (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH').
    - interval (str): The time interval for each candlestick (e.g., '1h', '4h', '1d').
    - limit (int): The quantity limit of candlesticks to retrieve.

    Returns:
    - dict: If successful, returns a dictionary containing candlestick data.
      The 'data' key contains a list of dictionaries, where each dictionary represents a candlestick.

    - str: If unsuccessful, returns an error message.
    """
    current_datetime = datetime.now()
    resultant_date = current_datetime - timedelta(days=limit)
    desired_time = datetime(resultant_date.year, resultant_date.month, resultant_date.day, 15, 59, 59)
    start_epoch_timestamp = int(str(int(desired_time.timestamp()))+'000')
    end_epoch_timestamp = int(str(int(time.time()))+'000')
    payload = {}
    path = '/openApi/spot/v1/market/kline'
    method = 'GET'
    params_map = {
    'symbol': symbol,
    'interval': interval, #(3m, 5m, 10m  = minute |  1h, 2h, 4h = hour | 1d, 3d, 8d = day | 1w, 2w, 8w = week | 1M, 2M, 6M = month)
    'startTime': start_epoch_timestamp,
    'endTime': end_epoch_timestamp,
    'limit' : limit #qty limit inverval
    }  
    params_str = credential.praseParam(params_map)
    json_data = json.loads(credential.send_request(method, path, params_str, payload))

    if 'data' in json_data:
        return json_data  
    else:
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))
        return error
    
'''
With the result of the candles function, it is possible to perform various types of 
calculations, such as moving averages, averages, and also calculate the RSI as shown 
in the function below.
'''
def rsi(symbol,limit):
    """
    Calculate the Relative Strength Index (RSI) for a given trading pair.

    Parameters:
    - symbol (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH').
    - limit (int): The quantity limit of historical data to calculate RSI.

    Returns:
    - float: If successful, returns the RSI (Relative Strength Index) value.
      RSI is a momentum oscillator that measures the speed and change of price movements.
      The value ranges from 0 to 100, where values above 70 indicate overbought conditions,
      and values below 30 indicate oversold conditions.
    """
    json_data = candles(symbol,'1d',limit)

    if 'data' in json_data:
      opening = []
      closing = []

      for i in json_data['data']:
          open = float(i[1])
          closed = float(i[4])
          opening.append(open)
          closing.append(closed)
                 
      daily_change = [closing[i] - opening[i] for i in range(len(opening))]
      positive_change = [max(0, change) for change in daily_change]
      negative_change = [-min(0, change) for change in daily_change]
      period = limit
      moving_average_gains = [np.mean(positive_change[:period])]
      moving_average_losses = [np.mean(negative_change[:period])]

      for i in range(period, len(daily_change)):
          gain = positive_change[i]
          loss = negative_change[i]
          
          moving_average_gains.append(((period - 1) * moving_average_gains[-1] + gain) / period)
          moving_average_losses.append(((period - 1) * moving_average_losses[-1] + loss) / period)

      rs = [moving_average_gains[i] / moving_average_losses[i] for i in range(len(moving_average_gains))]
      rsi = [100 - (100 / (1 + rs_value)) for rs_value in rs]
      rsi = rsi[0]
      return rsi  
    else:
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))