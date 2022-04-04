# coding: UTF-8

# python3 Test.py
from time import sleep
import config
import json
from web3 import Web3
from datetime import datetime

bsc_rpc = "https://bsc-dataseed.binance.org/"
PCSRouter = '0x10ED43C718714eb63d5aA57B78B54704E256024E'

harmony_rpc = "https://rpc.s0.t.hmny.io"
HarmonyRouter = '0x1b02da8cb0d097eb8d57a175b88c7d8b47997506'

walletAddress = config.WALLET_A
walletKey = config.KEY_A

gas = 189651
gasPrice = 31

rpc = harmony_rpc
router = HarmonyRouter
ADDRESS = "0x22fb638a010e922d53fd2671a598a3334c228b62"
ABIJson = 'ABI/JocABI.json'


web3 = Web3(Web3.HTTPProvider(rpc))

check_address = web3.toChecksumAddress(ADDRESS)
check_router = web3.toChecksumAddress(router)

with open(ABIJson) as f:
   abi = json.load(f)

contract = web3.eth.contract(address=check_address, abi=abi)

balance = contract.functions.totalSupply().call()

# balance = contract.functions.balanceOf(walletAddress).call()

print('Balance: {}'.format(web3.fromWei(balance,'ether')))