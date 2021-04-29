import os
import sys

import utils
import logging

from dotenv import set_key
from pathlib import Path
from discord.ext import commands
from config import DISCORD_TOKEN, AVATAR_HASH, cog_config

# LOGGING
logger = logging.getLogger("RocketRandy.main")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# RESOURCES
avatar_path = Path("resources/avatar.png")
disc_bot_client = commands.Bot(command_prefix="!")

# LOAD DISCORD COGS/EXTENSIONS
for root, dirs, files in os.walk("cogs"):
    for file_name in [file for file in files if file.endswith(".py")]:
        cog_name = Path(file_name).stem
        root = root.replace("\\", ".").replace("/", ".")
        logger.info(f"Loading {root}.{cog_name} extension...")
        disc_bot_client.cog_config = cog_config
        disc_bot_client.load_extension(f"{root}.{cog_name}")


@disc_bot_client.event
async def on_ready():
    # Check avatar
    if AVATAR_HASH != disc_bot_client.user.avatar:
        logger.info(f"Changing my avatar to {avatar_path}.")
        set_key(
            ".env", "AVATAR_HASH", await utils.set_avatar(disc_bot_client, avatar_path)
        )
    else:
        logger.info(f"No need to change my avatar, handsome as always")

    # Log basic info
    logger.info(f"{disc_bot_client.user} has connected to Discord!")


@disc_bot_client.command()
@commands.is_owner()
async def reload(ctx, extension_name: str):
    logger.info(f"Reloading extension: {extension_name}")
    disc_bot_client.reload_extension(extension_name)
    await ctx.send(
        f"{ctx.author.mention} I have reloaded the {extension_name} extension."
    )


##########

if __name__ == "__main__":
    disc_bot_client.run(DISCORD_TOKEN)
