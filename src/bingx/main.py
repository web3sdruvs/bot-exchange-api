import balance
import withdraw
import order
import candles

def get_balance():
    balance.balance('BTC') #(symbol)

def request_withdraw():
    withdraw.withdraw('BTC', 'Bitcoin', '0x00001', 'coldwallet', 1) #(symbol, network, address, addressTag, qty)

def create_order():
    order.create('BTC-USDT','BUY/SELL', 'MARKET/LIMIT', 'IOC/POC', 0.1, 90000) #(symbol, side, type, timeInForce, quoteOrderQty, price)

def cancel_order():
    order.cancel('BTC-USDT', 123456789) #(symbol, orderId)
''
def get_candles():
    candles.candles('BTC-USDT','1d',14) #(symbol,interval,limit) 