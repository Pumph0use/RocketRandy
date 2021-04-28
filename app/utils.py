import discord
from pathlib import Path


async def set_avatar(client: discord.client, avatar_path: Path):
    with open(avatar_path, "rb") as avatar_image:
        await client.user.edit(avatar=avatar_image.read())
        return client.user.avatar
