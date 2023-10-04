import credential
import json
import re

re_default = r'[^a-zA-Z0-9\s]'

def balance(symbol):
    payload = {}
    path = '/openApi/spot/v1/account/balance'
    method = 'GET'
    params_map = {
    'recvWindow': 0
    }
    params_str = credential.praseParam(params_map)
    json_data = json.loads(credential.send_request(method, path, params_str, payload))

    if 'data' in json_data:    
        for balance in json_data['data']['balances']:
            if balance['asset'] == symbol:
                amount = round(float(balance['free']),8)
                break
        return amount
    else: 
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))
        return  error