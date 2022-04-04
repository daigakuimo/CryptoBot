import json
import requests
import time
import hmac
import hashlib

class CoinCheck:
    def __init__(self, access_key, secret_key, url='https://coincheck.com'):
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
    def getTicker(self):
        URL = 'https://coincheck.com/api/ticker'
        ticker = requests.get(URL).json() 
        return ticker

    # 総資産
    def getBalance(self):
        path_balance = '/api/accounts/balance'
        result = self.get(path_balance)
        return result
    
    # 最新の取引履歴
    def getTrades(self, pair):
        URL = 'https://coincheck.com/api/trades'
        trades = requests.get(URL, params={"pair": pair}).json() 
        return trades

    # 板情報取得
    def getOrderBook(self):
        URL = 'https://coincheck.com/api/order_books'
        order_book = requests.get(URL).json() 
        return order_book

    """
    レート算出
    Args:
        order_type(string): sell or buy
        pair(string): only 'btc_jpy' now
        amount_or_price(string): 'amount' or 'price'
        value(float): num
    """
    def getOrdersRate(self, order_type, pair, amount_or_price, value):
        URL = 'https://coincheck.com/api/exchange/orders/rate'
        params = {'order_type': order_type, 'pair': pair, amount_or_price: value}
        orders_rate = requests.get(URL, params=params).json() 
        return orders_rate
    
    """
    新規注文：指値
    Args:
        pair(string): only 'btc_jpy' now
        order_type(string): sell or buy
        rate(float)
        amount(float)
    """
    def NewOrderForLimitPrice(self, pair, order_type, rate, amount):
        path_orders = '/api/exchange/orders'
        params = {
            "pair": pair,
            "order_type": order_type,
            "rate": rate,
            "amount": amount,
        }
        result = self.post(path_orders, params)
        return result

    """
    新規注文：成行
    Args:
        pair(string): only 'btc_jpy' now
        order_type(string): 'market_buy' or 'market_sell'
        amount(float)
    """
    def NewOrderForMarket(self, pair, order_type, amount):
        path_orders = '/api/exchange/orders'
        param = {}
        if(order_type == "market_buy"):
            params = {
                "pair": pair,
                "order_type": order_type,
                "market_buy_amount": amount,
            }
        else:
            params = {
                "pair": pair,
                "order_type": order_type,
                "amount": amount,
            }
        result = self.post(path_orders, params)
        return result

    # 未決済の注文一覧
    def getOrdersOpen(self):
        path_orders_opens = '/api/exchange/orders/opens'
        result = self.get(path_orders_opens)
        return result
    
    # 注文のキャンセル
    def deleteOrder(self, id):
        path_orders_cancel = '/api/exchange/orders/[id]'
        result = self.delete(path_orders_cancel)
        return result

    # 自分の最新の取引履歴
    def getTransactions(self):
        path = '/api/exchange/orders/transactions'
        result = self.get(path)
        return result

    # 最新の取引履歴
    def getTransactionsPagination(self):
        path = '/api/exchange/orders/transactions_pagination'
        result = self.get(path)
        return result

    # ビットコインを送金
    def sendBTC(self, address, amount):
        path_send_money = '/api/send_money'
        params = {
            "address": address,
            "amount": amount
        }
        result = self.post(path_send_money, params)
        return result
