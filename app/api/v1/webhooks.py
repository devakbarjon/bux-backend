from decimal import Decimal
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.users import get_user_by_id, update_user_adv_balance
from app.db.functions.transactions import save_transaction, get_transaction_by_id
from app.core.config import settings
from app.logging_config import logger
from app.services.bot.bot_base import bot


router = APIRouter()


@router.post("/ton-webhook")
async def ton_webhook(request: Request, session: AsyncSession = Depends(get_db)):
    payload = await request.json()
    query_params = dict(request.query_params)
    logger.info(payload, query_params)

    if query_params.get("secret") != settings.secret_key:
        return {"status": "unauthorized"}
    

    if payload.get("event") == "incoming_transaction":
        data = payload["data"]
        comment = data.get("comment", "")
        user_id = None
        if comment:
            user_id = int(comment)

            if user_id:
                user = await get_user_by_id(session, user_id)

                if user:
                    amount_ton = int(data["amount"]) / 1e9
                    sender = data["from"]
                    tx_hash = data["tx_hash"]

                    if tx_hash:
                        existing_transaction = await get_transaction_by_id(session, tx_hash)
                        if existing_transaction:
                            logger.info(f"Transaction {tx_hash} already exists.")
                            return {"status": "ok"}

                    await update_user_adv_balance(session, user_id, amount_ton)
                    
                    await save_transaction(
                        session=session,
                        user_id=user_id,
                        amount=Decimal(amount_ton),
                        status="completed",
                        transaction_id=tx_hash
                    )

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


    return {"status": "ok"}