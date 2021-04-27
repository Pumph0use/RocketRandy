import os
from dotenv import load_dotenv

load_dotenv()

# Database
DB_TYPE = os.getenv("DB_TYPE")
DB_DRIVER = os.getenv("DB_DRIVER")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")
DB_CONNECT_STRING = f"{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}"

# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AVATAR_HASH = os.getenv("AVATAR_HASH")
