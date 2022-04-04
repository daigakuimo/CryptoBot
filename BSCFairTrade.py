import json
from web3 import Web3
from datetime import datetime
import time
import config

bscRpc = "https://bsc-dataseed.binance.org/"
walletAddress = config.WALLET_A
walletKey = config.KEY_A

BUSD = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
CAKE = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'

PCSRouter = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
PCSFactory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'

gas = 500000
gasPrice = 10

targetToken = CAKE
targetAmountWBNB = 0.01
targetAmountBUSD = 6

web3 = Web3(Web3.HTTPProvider(bscRpc))

### Create Pancake Swap Router Contract ###
with open('ABI/PancakeABI.json') as f:
   pcsRouterABI = json.load(f)

pcsRouterContract = web3.eth.contract(address=PCSRouter, abi=pcsRouterABI)

### Create Pancake Swap Factory Contract ###
with open('ABI/PancakeFactoryABI.json') as f:
   pcsFactoryABI = json.load(f)

pcsFactoryContract = web3.eth.contract(address=PCSFactory, abi=pcsFactoryABI)

def checkLP( token1, token2 ):

   ### Get LP address ###
   lpAddr = pcsFactoryContract.functions.getPair( token1, token2 ).call()
   if web3.toInt(hexstr=lpAddr) == 0:
       return False
   else:
       return lpAddr

def waitLiquiditySupply( lpAddr, interval ):
   with open('ABI/PancakeLPABI.json') as f:
       pcsLPABI = json.load(f)

   pcsLPContract = web3.eth.contract(address=lpAddr, abi=pcsLPABI)

   while True:
       try:
           liq = pcsLPContract.functions.totalSupply().call()
           if liq > 0:
               return True
       except:
           print('error')

       time.sleep(interval)

def buyTokenETH( token, amountWBNB ):

   print('Swap WBNB to target token')
   now = int(datetime.now().timestamp())
   nonce = web3.eth.getTransactionCount(walletAddress)

   funcSwap = pcsRouterContract.functions.swapExactETHForTokens(
           0,
           [WBNB, token],
           walletAddress,
           now+300
           )

   tx = funcSwap.buildTransaction({
           'value': web3.toWei(amountWBNB, 'ether'),
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

   return status

def buyToken( token, amountBUSD ):

   print('Swap BUSD to target token')
   now = int(datetime.now().timestamp())
   nonce = web3.eth.getTransactionCount(walletAddress)

   funcSwap = pcsRouterContract.functions.swapExactTokensForTokens(
           web3.toWei(amountBUSD, 'ether'),
           0,
           [BUSD, token],
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

   return status

if __name__ == '__main__':

   lpAddedWBNB = False
   lpAddedBUSD = False

   print('Wait LP Pair...')
   while True:
       lpAddrWBNB = checkLP(targetToken, WBNB)
       lpAddrBUSD = checkLP(targetToken, BUSD)

       if lpAddrWBNB:
           print('Find LP Pair with BNB')
           print('Wait Liquidity...')
           waitLiquiditySupply(lpAddrWBNB, 0.5)
           print('Liquidity Added!')
           lpAddedWBNB = True
           break
       elif lpAddrBUSD:
           print('Find LP Pair with BUSD')
           print('Wait Liquidity...')
           waitLiquiditySupply(lpAddrBUSD, 0.5)
           print('Liquidity Added!')
           lpAddedBUSD = True
           break
       else:
           time.sleep(1)

   ### Buy Token ###
   if lpAddedWBNB:
       buyTokenETH( targetToken, targetAmountWBNB )
   elif lpAddedBUSD:
       buyToken( targetToken, targetAmountBUSD )