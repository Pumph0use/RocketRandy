import discord
from discord.ext import commands
from database.models.user import User
from database.models.responses import GreetingResponse
from database import Session


def add_user_to_session(session, member):
    user = User(member)
    session.add(user)
    return user


class DatabaseAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def dbadd(self, ctx):
        await ctx.send(f"This is a suite of test functions for the postgres database.")

    @dbadd.command()
    async def user(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        session = Session()

        user = session.query(User).filter(User.member_id == member.id).first()

        if user is None:
            add_user_to_session(session, member)
            session.commit()
            await ctx.send(
                f"{member.mention} user with ID:{member.id} and Display name:{member.display_name} stored in postgres."
            )

        else:
            await ctx.send(
                f"{member.mention} user with ID:{member.id} and Display name:{member.display_name} already in postgres."
            )

    @dbadd.command()
    async def greeting(self, ctx, *, response):
        session = Session()

        greeting = (
            session.query(GreetingResponse)
            .filter(GreetingResponse.response == response)
            .first()
        )

        user = session.query(User).filter(User.member_id == ctx.author.id).first()

        if user is None:
            user = User(ctx.author)

        if greeting is None:
            greeting = GreetingResponse(response)
            greeting.user = user
            session.add(greeting)
            session.commit()
            await ctx.send(
                f'{ctx.author.mention} I have added "{response}" to the Greetings database.'
            )


def setup(bot):
    bot.add_cog(DatabaseAdd(bot))
