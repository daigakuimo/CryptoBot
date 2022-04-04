import json
import requests
import time
import hmac
import hashlib
from enum import Enum


class GMO_COIN_SYMBOL(Enum):
    BTC= 1
    ETH = 2
    LTC = 3
    BCH = 4
    XRP = 5
    BTC_JPY = 6
    ETH_JPY = 7
    BCH_JPY = 8
    LTC_JPY = 9
    XRP_JPY = 10

class GMO:
    def __init__(self, access_key, secret_key, url='https://api.coin.z.com'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url

    def get(self, path, params=None):
        if params != None:
            params = json.dumps(params)
        else:
            params = ''
        nonce = str(int(time.time()))
        message = nonce + self.url + path + params

        signature = self.getSignature(message)

        return requests.get(
            self.url+path,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def post(self, path, params):
        params = json.dumps(params)
        nonce = str(int(time.time()))
        message = nonce + self.url + path + params

        signature = self.getSignature(message)

        return requests.post(
            self.url+path,
            data=params,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def delete(self, path):
        nonce = str(int(time.time()))
        message = nonce + self.url + path

        signature = self.getSignature(message)

        return requests.delete(
            self.url+path,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def getSignature(self, message):
        signature = hmac.new(
            bytes(self.secret_key.encode('ascii')),
            bytes(message.encode('ascii')),
            hashlib.sha256
        ).hexdigest()

        return signature

    def getHeader(self, access_key, nonce, signature):
        headers = {
            'ACCESS-KEY': access_key,
            'ACCESS-NONCE': nonce,
            'ACCESS-SIGNATURE': signature,
            'Content-Type': 'application/json'
        }

        return headers

     # 各種最新情報
    def getTicker(self, symbol):
        path = f'/public/v1/ticker?symbol={symbol}'
        print(path)
        result = self.get(path)
        return result


