import aiohttp
import discord
from discord.ext import commands


class UserManagement(commands.Cog):
    def __init__(self, bot, cog_config):
        self.bot = bot
        self.cog_config = cog_config

    @commands.command()
    async def get_member(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.cog_config["app_api"]}/users/{member.id}') as request:
                if request.status == 200:
                    await ctx.send(f'{ctx.author.mention} I have found the user you searched for.')
                elif request.status == 404:
                    await ctx.send(f'{ctx.author.mention} The user you searched for does not exist.')
                else:
                    await ctx.send(f'{ctx.author.mention} I have recieved a {request.status} code from the API.')

    @commands.command()
    @commands.is_owner()
    async def add_member(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.cog_config["app_api"]}/users/', json= {'id': member.id, 'display_name': member.display_name}) as request:
                if request.status == 204:
                    await ctx.send(f'{ctx.author.mention} I have added {member.display_name} to the database.')
                else:
                    await ctx.send(f'{ctx.author.mention} I have recieved a {request.status} code from the API.')


def setup(bot):
    bot.add_cog(UserManagement(bot, bot.cog_config))
