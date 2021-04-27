import discord
from discord.ext import commands
from database.models.user import User
from database.models.responses import GreetingResponse
from database import Session


class DatabaseRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def dbremove(self, ctx):
        await ctx.send(f"This is a suite of test functions for the postgres database.")

    @dbremove.command()
    async def user(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        session = Session()

        user = session.query(User).filter(User.discord_member_id == member.id).first()

        if user is not None:
            session.delete(user)
            session.commit()
            await ctx.send(
                f"{member.mention} user with ID:{member.id} and "
                f"Display name:{member.display_name} removed from User database."
            )

        else:
            await ctx.send(
                f"{member.mention} user with ID:{member.id} and "
                f"Display name:{member.display_name} is not stored in the User database."
            )

    @dbremove.command()
    async def greeting(self, ctx, *, response):
        session = Session()

        greeting = (
            session.query(GreetingResponse)
            .filter(GreetingResponse.response == response)
            .first()
        )

        if greeting is not None:
            session.delete(greeting)
            session.commit()
            await ctx.send(
                f'{ctx.author.mention} I have removed "{response}" from the Greetings database.'
            )
        else:
            await ctx.send(
                f"{ctx.author.mention} I can't seem to find '{response}' in the Greetings database."
            )


def setup(bot):
    bot.add_cog(DatabaseRemove(bot))
