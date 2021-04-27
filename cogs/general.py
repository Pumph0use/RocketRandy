import logging
import random

import discord
from discord.ext import commands
from database import Session
from database.models.responses import GreetingResponse
from database.models.user import User


async def get_random_greeting(session):
    greet_query = session.query(GreetingResponse)
    query_rows = int(greet_query.count())
    random_greeting = greet_query.offset(int(query_rows * random.random())).first()
    return random_greeting


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:

            session = Session()

            user = session.query(User).filter(User.member_id == member.id).first()

            if user is None:
                user = User(member)
                session.add(user)
                session.commit()

            random_greeting = await get_random_greeting(session)

            if random_greeting is not None:
                await channel.send(
                    random_greeting.response.replace("{member}", member.mention)
                )
            else:
                await channel.send(f"Welcome to our community {member.mention}!")

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
            random_greeting = await get_random_greeting(session)

            if random_greeting is not None:
                await ctx.send(
                    f"{random_greeting.response.replace('{member}', member.mention)}"
                )
            else:
                await ctx.send(f"Welcome to our community {ctx.author.mention}!")

        else:
            await ctx.send(f"Hello {member.mention}. I see you like attention.")
        self._last_member = member


def setup(bot):
    bot.add_cog(General(bot))
