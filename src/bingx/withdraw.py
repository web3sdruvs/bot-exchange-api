import credential
import json
import re

re_default = r'[^a-zA-Z0-9\s]'

'''
To utilize the withdrawal function, you need to set up the API with your public IP and configure 
the sending address along with the address tag on the exchange (you can find this in the withdrawal 
step on the exchange, next to the Address field, next the list icon)
'''
def withdraw(symbol, network, address, addressTag, qty, walletType):
    """
    Initiate a withdrawal request for a specific cryptocurrency.

    Parameters:
    - symbol (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH').
    - network (str): The network for the withdrawal (e.g., 'BTC', 'ERC20').
    - address (str): The destination address for the withdrawal.
    - addressTag (str): Address tag or memo for certain cryptocurrencies.
    - qty (float): The amount of cryptocurrency to withdraw.
    - walletType (str): 1 = fund account | 2 = standard account | 3 = perpetual account.

    Returns:
    - int: If successful, returns the withdrawal request ID.
    - str: If an error occurs, returns the error message.
    """
    payload = {}
    path = '/openApi/wallets/v1/capital/withdraw/apply'
    method = 'POST'
    params_map = {
    'coin': symbol,
    'network': network,
    'address': address,
    'addressTag': addressTag,
    'amount': qty,
    'walletType': walletType 
    }
    params_str = credential.praseParam(params_map)
    json_data = json.loads(credential.send_request(method, path, params_str, payload))

    if 'data' in json_data:  
        id = json_data['data']['id']
        return id
    else:
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))
        return  error

def withdrawfee(symbol, network):
    """
    Retrieve the withdrawal fee for a specific cryptocurrency and network.

    Parameters:
    - symbol (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH').
    - network (str): The network for the withdrawal (e.g., 'BTC', 'ERC20').

    Returns:
    - float: The withdrawal fee for the specified cryptocurrency and network.
    - str: If an error occurs, returns the error message.
    """
    payload = {}
    path = '/openApi/wallets/v1/capital/config/getall'
    method = "GET"
    params_map = {
    "recvWindow": 0
}
    params_str = credential.praseParam(params_map)
    json_data = json.loads(credential.send_request(method, path, params_str, payload))

    if 'data' in json_data:  
      json_data = json_data['data']
      for i in json_data:
        network_list = i.get("networkList", [])
        for fee  in network_list:
          if fee.get("name") == symbol and fee.get("network") == network:
            network_fee = fee['withdrawFee']
      return network_fee
    else: 
        error = json_data['msg']
        error = re.sub(re_default, ' ', str(error))
        return error