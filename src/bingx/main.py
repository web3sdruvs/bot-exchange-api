import balance
import withdraw
import order

balance.get_balance("BTC") #(symbol)
withdraw.request_withdraw("BTC", "Bitcoin", "0x00001", "coldwallet", 1) #(symbol, network, address, addressTag, qty)
order.create_order("BTC-USDT","BUY/SELL", "MARKET/LIMIT", "IOC/POC", 0.1, 90000) #(symbol, side, type, timeInForce, quoteOrderQty, price)
order.cancel_order("BTC-USDT", 123456789) #(symbol, orderId)