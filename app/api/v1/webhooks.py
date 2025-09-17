from decimal import Decimal
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.functions.users import get_user_by_id, update_user_adv_balance, update_user_balance
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

    if query_params.get("secret") != settings.secret_key:
        logger.warning("Unauthorized access attempt to TON webhook.")
        return {"status": "unauthorized"}
    
    if payload.get("event_type") == "account_tx":
        tx_hash = payload.get("tx_hash")
        if not tx_hash:
            logger.error("No tx_hash in payload")
            return {"status": "no tx_hash"}

        # Check for duplicates before fetching details
        if await get_transaction_by_id(session, tx_hash):
            logger.info(f"Transaction {tx_hash} already exists.")
            return {"status": "duplicate"}

        try:
            details = await fetch_transaction_details(tx_hash)
        except Exception as e:
            logger.error(f"Failed to fetch details for {tx_hash}: {e}")
            return {"status": "error_fetching_tx"}
        
        in_msg = details.get("in_msg", {})
        decoded_body = in_msg.get("decoded_body", {})
        comment = decoded_body.get("text", "")
        sender = in_msg.get("source")
        nanotons = int(in_msg.get("value", 0))
        amount_ton = Decimal(nanotons) / Decimal(1e9)

        # Credit user if comment contains user_id
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

                # Send Telegram notifications
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


@router.post("/flyer")
async def flyer_webhook(request: Request, session: AsyncSession = Depends(get_db)):
    query_params = dict(request.query_params)
    secret = query_params.get("secret")
    
    if secret != settings.secret_key:
        logger.warning("Unauthorized access attempt to Flyer webhook.")
        return {"status": "unauthorized"}
    
    data = await request.json()

    if data['type'] == 'new_status' and data['data']['status'] == 'abort':
        # User left the channel, applying penalty
        user_id = data['data']['user_id']
        penalty_amount = 10
        await update_user_balance(session, user_id, penalty_amount, increase=False)

    return {"status": "ok"}


@router.get("/adsgram")
async def adsgram_webhook(request: Request):
    query_params = dict(request.query_params)
    user_id = query_params.get("user_id")
    secret = query_params.get("secret")

    if secret != settings.secret_key or not user_id:
        logger.warning("Unauthorized access attempt to AdsGram webhook.")
        return {"status": "unauthorized"}
    
    return {"status": "ok"}