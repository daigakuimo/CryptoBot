# coding: UTF-8

# python3 Test.py
from time import sleep
import config
import json
from web3 import Web3
from datetime import datetime

bsc_rpc = "https://bsc-dataseed.binance.org/"
PCSRouter = '0x10ED43C718714eb63d5aA57B78B54704E256024E'

walletAddress = config.WALLET_A
walletKey = config.KEY_A

gas = 300000
gasPrice = 5

rpc = bsc_rpc
router = PCSRouter
ADDRESS = "0xa5496935A247fA81B1462E553ad139d2FD0af795"
ABIJson = 'ABI/FlagABI.json'


web3 = Web3(Web3.HTTPProvider(rpc))

### Create CAKE Token Contract ###
with open(ABIJson) as f:
   ABI = json.load(f)
cakeContract= web3.eth.contract(address=ADDRESS, abi=ABI)

### Approve ###
now = int(datetime.now().timestamp()) # get now unixtime
nonce = web3.eth.getTransactionCount(walletAddress) # get nonce
inf = 2**256 - 1
func = cakeContract.functions.approve(router, inf )
tx = func.buildTransaction({
   'value': 0,
   'gas': gas,
   'gasPrice': web3.toWei(gasPrice, 'gwei'),
   'nonce': nonce
   })
signedTx = web3.eth.account.sign_transaction(tx, walletKey)
txHash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
print('Send transaction')
print(web3.toHex(txHash))
result = web3.eth.wait_for_transaction_receipt(txHash)
status = result['status']
if status == 1:
   print('Transaction Succeeded')
else:
   print('Transaction Failed')