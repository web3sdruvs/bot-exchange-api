import balance
import withdraw

balance.get_balance("BTC") ##(symbol)
withdraw.request_withdraw("BTC", "Bitcoin", "0x00001", "coldwallet", 1) #(symbol, network, address, addressTag, qty)