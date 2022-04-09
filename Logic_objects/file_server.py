import config
from web3 import Web3
import os
import uuid
from flask import current_app


class File_server(object):
    def __init__(self, file_type) -> None:

        if file_type == "audio":
            self.folder = "audio"
        elif file_type == "image":
            self.folder = "image"
        elif file_type == "video":
            self.folder = "video"
        else:
            self.folder = None

    def save_file(self, file):
        if not self.folder:
            return
        self.file = file
        self.file_extension = file.filename.rsplit('.', 1)[1]
        filename = str(uuid.uuid4()) + "." + self.file_extension
        self.filename = filename

        path = str(os.getcwd() + f"/FILES/{self.folder}/")
        print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        self.file.save(os.path.join(path, filename))
        print(type(filename))
        return str(filename)


# test = file_server("audio" , 1)


class Reward():
    def __init__(self, user_wallet) -> None:
        self.ganache_url = config.GANACHE_URL
        self.web3 = Web3(Web3.HTTPProvider(self.ganache_url))
        self.contract_acc = config.CONTRACT
        self.private_key1 = config.PRIVATE_KEY
        self.user_wallet = user_wallet
        self.nonce = self.web3.eth.getTransactionCount(self.contract_acc)

    def sign_transaction(self):
        tx = {
            'nonce': self.nonce,
            'to': self.user_wallet,
            'value': self.web3.toWei(0.1, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        }

        signed_tx = self.web3.eth.account.sign_transaction(
            tx, self.private_key1)

        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return self.web3.toHex(tx_hash)

    def __repr__(self) -> str:
        return self.user_wallet
