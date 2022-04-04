# coding: UTF-8

# python3 Test.py
from time import sleep
import config
import json
from web3 import Web3
from datetime import datetime

harmony_rpc = "https://rpc.s0.t.hmny.io"

walletAddress = config.WALLET_A
walletKey = config.KEY_A

STAR = "0xb914e7a183abcd46300584da828f62a39516f33b"
SPEED = "0x2dae9ac8e3195715f308b59e7e9326f115ab4d98"
JOC = "0x22fb638a010e922d53fd2671a598a3334c228b62"
WONE = "0xcf664087a5bb0237a0bad6742852ec6c8d69a27a"

HarmonyRouter = '0x1b02da8cb0d097eb8d57a175b88c7d8b47997506'

gas = 190000
gasPrice = 31

web3 = Web3(Web3.HTTPProvider(harmony_rpc))

check_swap_from_address = web3.toChecksumAddress(WONE)
check_swap_to_address = web3.toChecksumAddress(SPEED)
check_router = web3.toChecksumAddress(HarmonyRouter)


with open('ABI/UniswapABI.json') as f:
   uniswapRouterABI = json.load(f)
pcsRouterContract = web3.eth.contract(address=check_router, abi=uniswapRouterABI)

now = int(datetime.now().timestamp()) # get now unixtime
nonce = web3.eth.getTransactionCount(walletAddress) # get nonce
funcSwap = pcsRouterContract.functions.swapExactTokensForTokens(
      1000000000000000000, # Amount
      0,
      [check_swap_from_address, check_swap_to_address],
      walletAddress,
      now+300
      )
tx = funcSwap.buildTransaction({
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