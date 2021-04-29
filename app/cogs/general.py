import logging
import random
import json

import discord
import emoji
from discord.ext import commands
import aiohttp


class General(commands.Cog):
    def __init__(self, bot, cog_config):
        self.bot = bot
        self._last_member = None
        self.cog_config = cog_config
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.Cog.listener("on_message")
    async def general_on_message(self, message):
        # Ignore bot's messages
        if message.author == self.bot.user:
            return

        elif "fuck you" in message.content:
            await message.channel.send(
                f"No. Fuck you {message.author.mention}, my good sir/madam!"
            )

        elif "im off the ceiling" in message.content.lower().strip("'`’"):
            await message.channel.send(f"{message.author.mention} I know you see me")

        elif len(message.mentions) > 0:
            if self.bot.user.id in [mention.id for mention in message.mentions]:
                await message.channel.send(f"{message.author.mention} Don't @ me bro!")

    @commands.command()
    async def cum(self, ctx, number: int = 20):
        # literally only because my discord server is weird and kept asking for it.
        # my bad.
        await ctx.send(emoji.emojize(f'{":sweat_drops:" * number}'))

    @commands.command()
    @commands.is_owner()
    async def api_test(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.cog_config['app_api']) as request:
                if request.status == 200:
                    await ctx.send(json.dumps(await request.json()))


def setup(bot):
    bot.add_cog(General(bot, bot.cog_config))
