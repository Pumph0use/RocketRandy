import os
from dotenv import load_dotenv

if os.getenv('APP_ENV') != 'compose':
    load_dotenv('.env')

# API
APP_API_HOST = os.getenv('APP_API_HOST')
APP_API_PORT = os.getenv('APP_API_PORT')
APP_API_URL = f'http://{APP_API_HOST}:{APP_API_PORT}'


# COG CONFIG
cog_config = {'app_api': APP_API_URL}


# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AVATAR_HASH = os.getenv("AVATAR_HASH")
