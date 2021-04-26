import discord
from discord.ext import commands
from database.models.user import User
from database import Session


class DatabaseTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def db(self, ctx):
        await ctx.send(f'This is a suite of test functions for the postgres database.')

    @db.command()
    async def add(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        session = Session()

        user = session.query(User).filter(User.discord_member_id == member.id).first()

        if user is None:
            user = User(member)
            session.add(user)
            session.commit()
            await ctx.send(f'{member.mention} user with ID:{member.id} and Display name:{member.display_name} stored in postgres.')

        else:
            await ctx.send(f'{member.mention} user with ID:{member.id} and Display name:{member.display_name} already in postgres.')


def setup(bot):
    bot.add_cog(DatabaseTools(bot))
