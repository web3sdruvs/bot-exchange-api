import credential
import json
import re

re_default = r'[^a-zA-Z0-9\s]'

'''
To utilize the withdrawal function, you need to set up the API with your public IP and configure 
the sending address along with the address tag on the exchange (you can find this in the withdrawal 
step on the exchange, next to the Address field, next the list icon)
'''
def withdraw(symbol, network, address, addressTag, qty):
    payload = {}
    path = '/openApi/wallets/v1/capital/withdraw/apply'
    method = 'POST'
    paramsMap = {
    'coin': symbol,
    'network': network,
    'address': address,
    'addressTag': addressTag,
    'amount': qty,
    'walletType': 1
    }
    paramsStr = credential.praseParam(paramsMap)
    json_data = json.loads(credential.send_request(method, path, paramsStr, payload))

    if 'data' in json_data:  
        id = json_data['data']['id']
        return id
    else:
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))
        return  error