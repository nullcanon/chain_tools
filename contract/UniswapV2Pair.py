
from web3 import Web3, HTTPProvider
import os
import json

def loadAbi(path):
    with open(path,"r") as f:
        load_dict = json.load(f)
    return load_dict["abi"]

class UniswapV2Pair:
    def __init__(self, config):
        self.w3 = Web3(Web3.HTTPProvider(config['rpc']))
        self.chainId = config['chainId']
        self.userAddress = config['address']
        self.userPirvateKey = config['private']
        basepath = os.path.abspath(__file__)
        folder = os.path.dirname(basepath)
        data_path = os.path.join(folder, 'abi', 'UniswapV2Pair.json')
        self.abi = loadAbi(data_path)
        self.contract = self.w3.eth.contract(address=config['contract'], abi=self.abi)
        self.gasPrice = config['gasPrice']

    def signedAndSendAndWaitTransaction(self, tx):
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=self.userPirvateKey)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

