from tonutils.client import ToncenterV3Client
from tonutils.wallet import (
    WalletV4R2,
)

from app.core.config import settings
IS_TESTNET = False

MNEMONIC = settings.mnemonic
API_KEY = settings.ton_center_api_key

client = ToncenterV3Client(api_key=API_KEY, is_testnet=IS_TESTNET, rps=1, max_retries=1)

wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(client, MNEMONIC)


class TonService:
    def __init__(self):
        self.wallet = wallet

    async def get_wallet_balance(self):
        """Get the balance of the wallet."""
        return await self.wallet.get_balance()

    async def send_transaction(self, to_address: str, amount: int):
        """Send TON to another address."""
        return await self.wallet.transfer(
            destination=to_address,
            amount=amount,
            body="Payment | @ton_bux_bot",
        )
    

TonServices = TonService()