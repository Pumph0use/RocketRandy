import json
import logging
import random

import discord
from discord.ext import commands
from database import Session
from database.models.responses import GreetingResponse


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            with open("resources/responses.json", "r") as in_file:
                responses = json.load(in_file)
                response = random.choice(responses["greetings"]).replace(
                    "%MEMBER%", member.mention
                )
                await channel.send(response)

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
    async def hello(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        if self._last_member is None or self._last_member != member.id:
            session = Session()
            greet_query = session.query(GreetingResponse)
            query_rows = int(greet_query.count())
            random_greeting = greet_query.offset(
                int(query_rows * random.random())
            ).first()

            if random_greeting is not None:
                await ctx.send(f"{random_greeting.response}")
            else:
                await ctx.send(
                    f"I don't seem to have any good greetings {ctx.author.mention}"
                )

        else:
            await ctx.send(f"Hello {member.mention}. I see you like attention.")
        self._last_member = member


def setup(bot):
    bot.add_cog(General(bot))
