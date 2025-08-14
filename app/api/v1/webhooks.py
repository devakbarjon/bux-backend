from decimal import Decimal
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.functions.users import get_user_by_id, update_user_adv_balance
from app.db.functions.transactions import save_transaction, get_transaction_by_id
from app.core.config import settings
from app.logging_config import logger
from app.services.bot.bot_base import bot
from app.services.ton.tonapi import fetch_transaction_details

router = APIRouter()


@router.post("/ton-webhook")
async def ton_webhook(request: Request, session: AsyncSession = Depends(get_db)):
    payload = await request.json()
    query_params = dict(request.query_params)

    logger.info(f"Webhook payload: {payload}")

    # 1. Verify secret key in query params
    if query_params.get("secret") != settings.secret_key:
        return {"status": "unauthorized"}

    # 2. Process only account_tx events
    if payload.get("event_type") == "account_tx":
        tx_hash = payload.get("tx_hash")
        if not tx_hash:
            logger.error("No tx_hash in payload")
            return {"status": "no tx_hash"}

        # 3. Check for duplicates before fetching details
        if await get_transaction_by_id(session, tx_hash):
            logger.info(f"Transaction {tx_hash} already exists.")
            return {"status": "duplicate"}

        try:
            # 4. Get transaction details from TonAPI
            details = await fetch_transaction_details(tx_hash)
        except Exception as e:
            logger.error(f"Failed to fetch details for {tx_hash}: {e}")
            return {"status": "error_fetching_tx"}

        # 5. Extract needed data from details
        in_msg = details.get("in_msg", {})
        logger.info(in_msg)
        comment = in_msg.get("message", "")
        sender = in_msg.get("source")
        nanotons = int(in_msg.get("value", 0))
        amount_ton = Decimal(nanotons) / Decimal(1e9)

        # 6. Credit user if comment contains user_id
        if comment.isdigit():
            user_id = int(comment)
            user = await get_user_by_id(session, user_id)
            if user:
                await update_user_adv_balance(session, user_id, amount_ton)
                await save_transaction(
                    session=session,
                    user_id=user_id,
                    amount=amount_ton,
                    status="completed",
                    transaction_id=tx_hash
                )

                # 7. Send Telegram notifications
                try:
                    await bot.send_message(
                        chat_id=settings.admin_chat_id,
                        text=f"New deposit: {amount_ton} TON from {sender} (User ID: {user_id})"
                    )
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"Your account has been credited with {amount_ton} TON."
                    )
                except Exception as e:
                    logger.error(f"Failed to send message to user {user_id}: {e}")
        else:
            logger.warning(f"Transaction {tx_hash} has no valid user ID in comment")

    return {"status": "ok"}
