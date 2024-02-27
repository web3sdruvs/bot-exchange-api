import credential
import json
import re

re_default = r'[^a-zA-Z0-9\s]'

#create an order
def create(symbol, side, type, timeInForce, quoteOrderQty, price):
    """
    Create a new trade order in the spot market.

    Parameters:
    - symbol (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH').
    - side (str): The order side, either 'BUY' or 'SELL'.
    - type (str): The order type, either 'MARKET' or 'LIMIT'.
    - timeInForce (str): The time in force for the order, options are 'IOC' (immediate-or-cancel) or 'POC' (process-or-cancel).
    - quoteOrderQty (float): The quote order quantity.
    - price (float, optional): The limit price for a 'LIMIT' order. If not provided, a 'MARKET' order is placed.

    Returns:
    - tuple: If successful, returns a tuple containing orderId, priceOrder, qty, total, and status.
        - orderId (int): The unique identifier for the order.
        - priceOrder (float): The price at which the order was executed.
        - qty (float): The executed quantity of the order.
        - total (float): The total value of the order (qty * priceOrder).
        - status (str): The status of the order (e.g., 'filled', 'partially-filled', 'rejected').

    - str: If unsuccessful, returns an error message.
    """
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
    """
    Cancel a specific order for a given cryptocurrency symbol.

    Parameters:
    - symbol (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH').
    - orderId (int): The ID of the order to be canceled.

    Returns:
    - int: If successful, returns the client order ID of the canceled order.
    - str: If an error occurs, returns the error message.
    """
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
       