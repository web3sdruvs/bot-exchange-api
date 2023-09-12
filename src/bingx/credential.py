import time
import requests
import hmac
from hashlib import sha256

#when creating an API, remember to configure only your access IP for security reasons and also to enable other features such as withdrawals.
APIURL_BINGX = 'https://open-api.bingx.com'
APIKEY_BINGX = 'YOUR API KEY'
SECRETKEY_BINGX = 'YOUR SECRET KEY'

#get sign request secretkey to generate a signature
def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode('utf-8'), payload.encode('utf-8'), digestmod=sha256).hexdigest()
    return signature

#single request api call
def send_request(method, path, urlpa, payload):
    url = '%s%s?%s&signature=%s' % (APIURL_BINGX, path, urlpa, get_sign(SECRETKEY_BINGX, urlpa))
    headers = {
        'X-BX-APIKEY': APIKEY_BINGX,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

#parameter encapsulation
def praseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = '&'.join(['%s=%s' % (x, paramsMap[x]) for x in sortedKeys])
    return paramsStr+'&timestamp='+str(int(time.time() * 1000))