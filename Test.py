# coding: UTF-8
import requests
import json
import CoinCheck
import GMO
import config
from websocket import create_connection



access_key = config.GMO_ACCESS_KEY
secret_key = config.GMO_SECRET_KEY

gmo = GMO.GMO(secret_key, secret_key)

result = gmo.getTicker()
print(result)


# coincheck = CoinCheck.CoinCheck(access_key,secret_key)

# result = coincheck.getTransactionsPagination()
# print(result)


# ws = create_connection("wss://ws-api.coincheck.com/")

# ws.send(json.dumps({
#    "type": "subscribe",
#    "channel": "btc_jpy-orderbook"
# }))

# while True:
#    print (ws.recv())
