from app.logging_config import logger
from .bot_base import bot


async def check_bot_subscription(user_id: int, channel_id: int) -> bool:
    """
    Check if the user is subscribed to the bot's channel.
    
    Args:
        user_id (int): The Telegram user ID.
        channel_id (int): The Telegram channel ID to check subscription against.
    
    Returns:
        int: True if the user is subscribed, False otherwise.
    """
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking subscription for user {user_id}: {e}")
        return False