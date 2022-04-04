import json
from web3 import Web3
from datetime import datetime
import time
import config

harmonyRpc = "https://rpc.s0.t.hmny.io"
walletAddress = config.WALLET_A
walletKey = config.KEY_A

STAR = "0xb914e7a183abcd46300584da828f62a39516f33b"
SPEED = "0x2dae9ac8e3195715f308b59e7e9326f115ab4d98"
JOC = "0x22fb638a010e922d53fd2671a598a3334c228b62"
WONE = "0xcf664087a5bb0237a0bad6742852ec6c8d69a27a"

HarmonyRouter = '0x1b02da8cb0d097eb8d57a175b88c7d8b47997506'
HarmonyFactory = '0xc35DADB65012eC5796536bD9864eD8773aBc74C4'

gas = 190000
gasPrice = 31


targetToken = JOC
targetAmountWONE = 4000

web3 = Web3(Web3.HTTPProvider(harmonyRpc))

### Create Pancake Swap Router Contract ###
with open('ABI/UniswapABI.json') as f:
   uniswapRouterABI = json.load(f)

uniswapRouterContract = web3.eth.contract(address=web3.toChecksumAddress(HarmonyRouter), abi=uniswapRouterABI)

### Create Pancake Swap Factory Contract ###
with open('ABI/UniswapFactoryABI.json') as f:
   uniswapFactoryABI = json.load(f)

uniswapFactoryContract = web3.eth.contract(address=web3.toChecksumAddress(HarmonyFactory), abi=uniswapFactoryABI)

def checkLP( token1, token2 ):
   ### Get LP address ###
   lpAddr = uniswapFactoryContract.functions.getPair( token1, token2 ).call()
   if web3.toInt(hexstr=lpAddr) == 0:
       return False
   else:
       return lpAddr

def waitLiquiditySupply( lpAddr, interval ):
   with open('ABI/SushiLPABI.json') as f:
       uniswapLPABI = json.load(f)

   uniswapLPContract = web3.eth.contract(address=lpAddr, abi=uniswapLPABI)

   while True:
       try:
           liq = uniswapLPContract.functions.totalSupply().call()
           if liq > 0:
               return True
       except:
           print('error')

       time.sleep(interval)

# def buyTokenETH( token, amountWBNB ):

#    print('Swap WBNB to target token')
#    now = int(datetime.now().timestamp())
#    nonce = web3.eth.getTransactionCount(walletAddress)

#    funcSwap = uniswapRouterContract.functions.swapExactETHForTokens(
#            0,
#            [WBNB, token],
#            walletAddress,
#            now+300
#            )

#    tx = funcSwap.buildTransaction({
#            'value': web3.toWei(amountWBNB, 'ether'),
#            'gas': gas,
#            'gasPrice': web3.toWei(gasPrice, 'gwei'),
#            'nonce': nonce
#            })

#    signedTx = web3.eth.account.sign_transaction(tx, walletKey)
#    txHash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
#    print('Send transaction')
#    print(web3.toHex(txHash))

#    result = web3.eth.wait_for_transaction_receipt(txHash)

#    status = result['status']
#    if status == 1:
#        print('Transaction Succeeded')
#    else:
#        print('Transaction Failed')

#    return status

def buyToken( token, amountWONE ):

   print('Swap WONE to target token')
   now = int(datetime.now().timestamp())
   nonce = web3.eth.getTransactionCount(walletAddress)

   funcSwap = uniswapRouterContract.functions.swapExactTokensForTokens(
           web3.toWei(amountWONE, 'ether'),
           0,
           [web3.toChecksumAddress(WONE), web3.toChecksumAddress(token)],
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

   return status

if __name__ == '__main__':

   lpAddedWBNB = False
   lpAddedBUSD = False

   print('Wait LP Pair...')
   while True:
       lpAddrWONE = checkLP(web3.toChecksumAddress(targetToken), web3.toChecksumAddress(WONE))

       if lpAddrWONE:
           print('Find LP Pair with WONE')
           print('Wait Liquidity...')
           waitLiquiditySupply(lpAddrWONE, 0.5)
           print('Liquidity Added!')
           lpAddedWONE = True
           break
       else:
           time.sleep(1)

   ### Buy Token ###
   if lpAddedWONE:
       buyToken( targetToken, targetAmountWONE )