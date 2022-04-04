# coding: UTF-8

# python3 Test.py
from time import sleep
import config
import json
from web3 import Web3
from datetime import datetime

bsc_rpc = "https://bsc-dataseed.binance.org/"

walletAddress = config.WALLET_A
walletKey = config.KEY_A

FLAG = "0xa5496935A247fA81B1462E553ad139d2FD0af795"
WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
BUSD = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
PCSRouter = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
gas = 300000
gasPrice = 5

balance = 0
lockBalance = 0
lastBalance = 0
lastLockBalance = 0

web3 = Web3(Web3.HTTPProvider(bsc_rpc))

while(1):
   web3 = Web3(Web3.HTTPProvider(bsc_rpc))

   with open('ABI/FlagABI.json') as f:
      abi = json.load(f)

   contract = web3.eth.contract(address=FLAG, abi=abi)

   balance = contract.functions.balanceOf(walletAddress).call()
   lockBalance = contract.functions.lockBalanceOf(walletAddress).call()

   print('Flag Balance: {}'.format(web3.fromWei(balance,'ether')))
   print('Flag lockBalance: {}'.format(web3.fromWei(lockBalance,'ether')))

   if(lockBalance < lastLockBalance):
      break

   lastBalance = balance
   lastLockBalance = lockBalance

   sleep(1)



### Create Pancake Swap Router Contract ###
with open('ABI/PancakeABI.json') as f:
   pcsRouterABI = json.load(f)
pcsRouterContract = web3.eth.contract(address=PCSRouter, abi=pcsRouterABI)

### Swap BUSD to FLAG ###
now = int(datetime.now().timestamp()) # get now unixtime
nonce = web3.eth.getTransactionCount(walletAddress) # get nonce
funcSwap = pcsRouterContract.functions.swapExactTokensForTokens(
      balance - lockBalance, #BUSD Amount
      0,
      [FLAG, WBNB],
      walletAddress,
      now+300
      )
tx = funcSwap.buildTransaction({
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