import time
import requests
import hmac
from hashlib import sha256

#when creating an API, remember to configure only your access IP for security reasons and also to enable other features such as withdrawals.
#warning: This code is for example purposes only and should not be used in production.
#storing credentials directly in the code is not secure and can expose sensitive information.
#in real environments, use environment variables or a secrets manager to protect your credentials.
APIURL_BINGX = 'https://open-api.bingx.com'
APIKEY_BINGX = 'YOUR API KEY' #example only, do not hardcode in production
SECRETKEY_BINGX = 'YOUR SECRET KEY' #example only, do not hardcode in production

def get_sign(api_secret, payload):
    """
    Generate a signature for authenticating an API request.

    Parameters:
    - api_secret (str): API secret key.
    - payload (str): Request data to be signed.

    Returns:
    - str: Generated signature as a hexadecimal string.
    """
    signature = hmac.new(api_secret.encode('utf-8'), payload.encode('utf-8'), digestmod=sha256).hexdigest()
    return signature

def send_request(method, path, urlpa, payload):
    """
    Make a call to the BingX API.

    Parameters:
    - method (str): HTTP method of the request (e.g., 'GET', 'POST').
    - path (str): API endpoint path.
    - urlpa (str): URL parameters.
    - payload (str): Request data.

    Returns:
    - str: Content of the API response.
    """
    url = '%s%s?%s&signature=%s' % (APIURL_BINGX, path, urlpa, get_sign(SECRETKEY_BINGX, urlpa))
    headers = {
        'X-BX-APIKEY': APIKEY_BINGX,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def praseParam(params_map):
    """
    Encapsulate parameters in a specific format for an API request.

    Parameters:
    - params_map (dict): Dictionary containing the request parameters.

    Returns:
    - str: Formatted string of parameters with timestamp added.
    """
    sortedKeys = sorted(params_map)
    params_str = '&'.join(['%s=%s' % (x, params_map[x]) for x in sortedKeys])
    return params_str+'&timestamp='+str(int(time.time() * 1000))