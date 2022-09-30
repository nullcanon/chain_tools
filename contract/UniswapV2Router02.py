
from web3 import Web3, HTTPProvider
import os
import json

def loadAbi(path):
    with open(path,"r") as f:
        load_dict = json.load(f)
    return load_dict["abi"]

class UniswapV2Router02:
    def __init__(self, config):
        self.w3 = Web3(Web3.HTTPProvider(config['rpc']))
        self.chainId = config['chainId']
        self.userAddress = config['address']
        self.userPirvateKey = config['private']
        basepath = os.path.abspath(__file__)
        folder = os.path.dirname(basepath)
        data_path = os.path.join(folder, 'abi', 'UniswapV2Router02.json')
        self.abi = loadAbi(data_path)
        self.contract = self.w3.eth.contract(address=config['contract'], abi=self.abi)
        self.gasPrice = config['gasPrice']

    def signedAndSendAndWaitTransaction(self, tx):
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=self.userPirvateKey)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)




    def swapExactTokensForTokens(self, swapRouterAddress, addressPath, fromAmount):
        if fromAmount < 1000:
            return
        uniswap_contract = self.w3.eth.contract(address=swapRouterAddress, abi=self.uniswapV2Router02Abi)
        uniswap_txn = uniswap_contract.functions.swapExactTokensForTokens(
            fromAmount,
            0,
            addressPath,
            # self.userAddress,
            self.toAddress,
            int(time.time()) + 100000000
        ).buildTransaction({
            'chainId': chainId,
            'nonce': self.w3.eth.get_transaction_count(self.userAddress),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('1', 'gwei')
        })
        self.signedAndSendAndWaitTransaction(tx = uniswap_txn)