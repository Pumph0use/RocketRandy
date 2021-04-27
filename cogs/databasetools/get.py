import discord
from discord.ext import commands
from database.models.user import User
from database.models.responses import GreetingResponse
from database import Session


class DatabaseGet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def dbget(self, ctx):
        await ctx.send(f"This is a suite of test functions for the postgres database.")

    @dbget.command()
    async def user(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        session = Session()

        user = session.query(User).filter(User.member_id == member.id).first()

        if user is not None:
            await ctx.send(
                f"{member.mention} user with ID:{user.member_id} and "
                f"Display name:{user.display_name} was first seen on {user.date_first_seen}."
            )

        else:
            await ctx.send(f"{member.mention} no user found in the database.")

    @dbget.command()
    async def greeting(self, ctx, *, response):
        session = Session()

        greeting = (
            session.query(GreetingResponse)
            .filter(GreetingResponse.response == response)
            .first()
        )

        if greeting is not None:
            await ctx.send(
                f"{ctx.author.mention} I have found a Greeting with ID:{greeting.id}, "
                f'Response:"{greeting.response}", '
                f"and it was added by {greeting.user.display_name} from the database."
            )
        else:
            await ctx.send(
                f"{ctx.author.mention} I can't seem to find '{response}' in the Greetings database."
            )


def setup(bot):
    bot.add_cog(DatabaseGet(bot))
