import httpx
from app.core.config import settings


TONAPI_BASE = "https://tonapi.io/v2"  # Main TonAPI endpoint for fetching details


async def fetch_transaction_details(tx_hash: str):
    """Fetch full transaction data from TonAPI."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{TONAPI_BASE}/blockchain/transactions/{tx_hash}",
            headers={"Authorization": f"Bearer {settings.tonapi_key}"}
        )
        resp.raise_for_status()
        return resp.json()