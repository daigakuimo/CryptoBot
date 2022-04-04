# coding: UTF-8

# python3 HarmonyApprove.py
# Make sure you have $One.

from time import sleep
import config
import json
from web3 import Web3
from datetime import datetime

harmony_rpc = "https://rpc.s0.t.hmny.io"
HarmonyRouter = '0x1b02da8cb0d097eb8d57a175b88c7d8b47997506'

walletAddress = config.WALLET_A
walletKey = config.KEY_A

gas = 190000
gasPrice = 31

rpc = harmony_rpc
router = HarmonyRouter
ADDRESS = "0xcf664087a5bb0237a0bad6742852ec6c8d69a27a"
ABIJson = 'ABI/OneABI.json'

web3 = Web3(Web3.HTTPProvider(rpc))

check_address = web3.toChecksumAddress(ADDRESS)
check_router = web3.toChecksumAddress(router)

with open(ABIJson) as f:
   ABI = json.load(f)
contract = web3.eth.contract(address=check_address, abi=ABI)

### Approve ###
now = int(datetime.now().timestamp()) # get now unixtime
nonce = web3.eth.getTransactionCount(walletAddress) # get nonce
inf = 5000000000000000000000
func = contract.functions.approve(check_router, inf)

tx = func.buildTransaction({
    'gas' : gas,
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