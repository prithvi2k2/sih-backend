from web3 import Web3
import config


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
