import secrets
import string
from app.services.bot.bot_base import bot
from urllib.parse import urlparse


async def generate_random_key(length=5):
    alphabet = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))


async def classify_telegram_link(link: str) -> str:
    """
    Classify a Telegram link as 'bot', 'channel', or 'webapp'.
    Groups/supergroups are also treated as 'channel'.
    """

    # --- 1. Parse link ---
    parsed = urlparse(link)
    if parsed.netloc != "t.me":
        return "not_telegram"

    path = parsed.path.strip("/")  # e.g., MyCoolBot, examplechannel, +abc123
    query = parsed.query           # e.g., start=123

    # --- 2. Check if it's a WebApp ---
    if "startapp" in link:
        return "webapp"

    # --- 3. Check if it's a bot (username ends with Bot OR has start param) ---
    if path.lower().endswith("bot") or "start=" in query:
        return "bot"

    # --- 4. Otherwise, check with Bot API if it’s a channel/group ---
    try:
        chat = await bot.get_chat(chat_id=path)
        if chat.type in ["channel", "supergroup"]:
            return "channel"
    except Exception:
        pass

    return "channel"