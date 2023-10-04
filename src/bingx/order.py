import credential
import json
import re

re_default = r'[^a-zA-Z0-9\s]'

#create an order
def create(symbol, side, type, timeInForce, quoteOrderQty, price):
    payload = {}
    path = '/openApi/spot/v1/trade/order'
    method = 'POST'
    params_map = {
    'symbol': symbol,
    'side': side, #BUY/SELL
    'type': type, #MARKET/LIMIT
    'timeInForce': timeInForce, #IOC = immediate-or-cancel , POC = process-or-cancel
    'quoteOrderQty': quoteOrderQty,
    "price": price, #Price is not a mandatory field. If you want to buy at market price, you can exclude the price item from the function
    'recvWindow': 0
    }
    params_str = credential.praseParam(params_map)
    json_data = json.loads(credential.send_request(method, path, params_str, payload))

    if 'data' in json_data:
        orderId = json_data['data']['orderId']
        priceOrder = round(float(json_data['data']['price']),3)
        qty = float(json_data['data']['executedQty'])
        status = str(json_data['data']['status']).lower()
        total = round(qty*priceOrder,3)
        return orderId, priceOrder, qty, total, status 
    else:
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))
        return error

#cancel an order
def cancel(symbol, orderId):
    payload = {}
    path = '/openApi/spot/v1/trade/cancel'
    method = 'POST'
    params_map = {
    'symbol': symbol,
    'orderId': orderId,
    'recvWindow': 0
    }
    params_str = credential.praseParam(params_map)
    json_data = json.loads(credential.send_request(method, path, params_str, payload))
    
    if 'data' in json_data:
        clientOrderID = json_data['data']['clientOrderID']
        return clientOrderID
    else: 
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))
        return error
       