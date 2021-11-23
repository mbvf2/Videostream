import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Video Stream")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
OWNER_NAME = getenv("OWNER_NAME", "Shailendra34")
ALIVE_NAME = getenv("ALIVE_NAME", "Shailendra")
BOT_USERNAME = getenv("BOT_USERNAME", "heromusics_bot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "mai_hu_hero")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "yaaro_ki_yaarii")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "modmenumaking")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://te.legra.ph/file/a1dd253ae11053bfebaa3.png")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "900"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Shailendra34/Videostream")
IMG_1 = getenv("IMG_1", "https://te.legra.ph/file/a1dd253ae11053bfebaa3.png")
IMG_2 = getenv("IMG_2", "https://te.legra.ph/file/a1dd253ae11053bfebaa3.png")
IMG_3 = getenv("IMG_3", "https://te.legra.ph/file/a1dd253ae11053bfebaa3.png")
