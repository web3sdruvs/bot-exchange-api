import requests
import hmac
from hashlib import sha256

APIURL = 'https://api-testnet.bybit.com'
APIKEY = 'API_KEY'
SECRETKEY = 'SECRET_KEY'
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