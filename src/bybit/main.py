import balance
import withdraw
import order

'''
The data used to call the functions within the modules 
are examples and should be edited according to your needs.
'''
def get_balance():
    balance.balance('BTC') #(symbol)

def get_withdraw_fee():
    withdraw.withdrawfee("BTC", "BTC") #(symbol, network)

def request_withdraw():
    withdraw.withdraw('BTC', 'Bitcoin', '0x00001', 'coldwallet', 1, 1) #(symbol, network, address, addressTag, qty, walletType)

def create_order():
    order.create('BTC-USDT','BUY/SELL', 'MARKET/LIMIT', 'IOC/POC', 0.1, 90000) #(symbol, side, type, timeInForce, quoteOrderQty, price)

def cancel_order():
    order.cancel('BTC-USDT', 123456789) #(symbol, orderId)