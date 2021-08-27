# coding: UTF-8
import requests
import json
import CoinCheck
import config
from websocket import create_connection

access_key = config.ACCESS_KEY
secret_key = config.SECRET_KEY

coincheck = CoinCheck.CoinCheck(access_key,secret_key)

result = coincheck.getOrdersRate("sell", "btc_jpy", "amount", 0.00001)
print(result)


# ws = create_connection("wss://ws-api.coincheck.com/")

# ws.send(json.dumps({
#    "type": "subscribe",
#    "channel": "btc_jpy-orderbook"
# }))

# while True:
#    print (ws.recv())
