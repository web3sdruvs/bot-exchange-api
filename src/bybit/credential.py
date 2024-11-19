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