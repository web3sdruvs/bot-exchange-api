import time
import requests
import hmac
from hashlib import sha256

#when creating an API, remember to configure only your access IP for security reasons and also to enable other features such as withdrawals.
#warning: This code is for example purposes only and should not be used in production.
#storing credentials directly in the code is not secure and can expose sensitive information.
#in real environments, use environment variables or a secrets manager to protect your credentials.
APIURL = 'https://api-testnet.bybit.com'
APIKEY = 'API_KEY' #example only, do not hardcode in production
SECRETKEY = 'SECRET_KEY' #example only, do not hardcode in production
RECV_WINDOW = '5000'  # Receive window
httpClient = requests.Session()

def get_sign(api_secret, payload):
    """
    Generates a signature to authenticate an API request.

    Parameters:
    - api_secret (str): API secret key.
    - payload (str): Request data to be signed.

    Returns:
    - str: Generated signature as a hexadecimal string.
    """
    signature = hmac.new(api_secret.encode('utf-8'), payload.encode('utf-8'), digestmod=sha256).hexdigest()
    return signature

def send_request(method, path, params, payload):
    """
    Makes a call to the Bybit API.

    Parameters:
    - method (str): HTTP method (e.g., 'GET', 'POST').
    - path (str): API endpoint path.
    - params (dict): URL parameters.
    - payload (str): Request data (JSON).
    - info (str): Additional information for logging.

    Returns:
    - str: Content of the API response.
    """
    timestamp = str(int(time.time() * 1000))
    urlpa = praseParam(params, timestamp)
    signature = get_sign(SECRETKEY, urlpa)

    headers = {
        'X-BAPI-API-KEY': APIKEY,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': timestamp,
        'X-BAPI-RECV-WINDOW': RECV_WINDOW,
        'Content-Type': 'application/json'
    }
    url = f"{APIURL}{path}?{urlpa}&signature={signature}"

    try:
        response = requests.request(method, url, headers=headers, data=payload)
        response.raise_for_status()  # Checks for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        return None

def praseParam(params_map, timestamp):
    """
    Organizes and adds the timestamp to request parameters.

    Parameters:
    - params_map (dict): Dictionary with request parameters.
    - timestamp (str): Current request timestamp.

    Returns:
    - str: Formatted string of parameters with timestamp added.
    """
    sorted_keys = sorted(params_map)
    params_str = '&'.join(f"{key}={params_map[key]}" for key in sorted_keys)
    return f"{params_str}&timestamp={timestamp}&recv_window={RECV_WINDOW}"