import balance
import withdraw
import order

balance.get_balance("BTC") #(symbol)
withdraw.request_withdraw("BTC", "Bitcoin", "0x00001", "coldwallet", 1) #(symbol, network, address, addressTag, qty)
order.create_order("BTC", 0.1) #(symbol, quantity)
order.create_order("BTC", 123456789) #(symbol, orderId)