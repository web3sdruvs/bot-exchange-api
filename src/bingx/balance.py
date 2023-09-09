import credential
import json
import re

re_default = r'[^a-zA-Z0-9\s]'

def get_balance(symbol):
    payload = {}
    path = '/openApi/spot/v1/account/balance'
    method = 'GET'
    paramsMap = {
    'recvWindow': 0
    }
    paramsStr = credential.praseParam(paramsMap)
    json_data = json.loads(credential.send_request(method, path, paramsStr, payload))

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