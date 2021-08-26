# coding: UTF-8
import requests
import json
import CoinCheck
import config

access_key = config.ACCESS_KEY
secret_key = config.SECRET_KEY

coincheck = CoinCheck.CoinCheck(access_key,secret_key)

path_balance = '/api/accounts/balance'
result = coincheck.get(path_balance)
print(result)