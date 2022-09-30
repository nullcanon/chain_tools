
from web3 import Web3, HTTPProvider
import os
import json
import sys
sys.path.append("..")
from contract.common.utils import *
# from common.utils import *

# def loadAbi(path):
#     with open(path,"r") as f:
#         load_dict = json.load(f)
#     return load_dict["abi"]

class ERC20:
    def __init__(self, config):
        self.w3 = Web3(Web3.HTTPProvider(config['rpc']))
        self.chainId = config['chainId']
        self.userAddress = config['address']
        self.userPirvateKey = config['private']
        basepath = os.path.abspath(__file__)
        folder = os.path.dirname(basepath)
        data_path = os.path.join(folder, 'abi', 'ERC20.json')
        self.abi = loadAbi(data_path)
        self.contract = self.w3.eth.contract(address=config['contract'], abi=self.abi)
        self.gasPrice = config['gasPrice']

    def signedAndSendAndWaitTransaction(self, tx):
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=self.userPirvateKey)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def balanceOf(self, account):
        return self.contract.functions.balanceOf(account).call()


    def transfer(self, recipient, amount):
        tx = self.contract.functions.transfer(recipient, amount).buildTransaction({
            'chainId': self.chainId,
            'nonce': self.w3.eth.get_transaction_count(self.userAddress),
            'gas': 2000000,
            'gasPrice': self.w3.toWei(self.gasPrice, 'gwei')
        })
        self.signedAndSendAndWaitTransaction(tx = tx)

    def allowance(self, owner, spender):
        return self.contract.functions.allowance(owner, spender).call()

    def approve(self, spender, amount):
        tx = self.contract.functions.approve(spender, amount).buildTransaction({
            'chainId': self.chainId,
            'nonce': self.w3.eth.get_transaction_count(self.userAddress),
            'gas': 2000000,
            'gasPrice': self.w3.toWei(self.gasPrice, 'gwei')
        })
        self.signedAndSendAndWaitTransaction(tx = tx)

    def transferFrom(self, sender, recipient, amount):
        tx = self.contract.functions.transferFrom(spender, recipient, amount).buildTransaction({
            'chainId': self.chainId,
            'nonce': self.w3.eth.get_transaction_count(self.userAddress),
            'gas': 2000000,
            'gasPrice': self.w3.toWei(self.gasPrice, 'gwei')
        })
        self.signedAndSendAndWaitTransaction(tx = tx)