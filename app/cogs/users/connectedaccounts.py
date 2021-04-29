from discord.ext import commands


class ConnectedAccounts(commands.Cog):
    def __init__(self, bot, cog_config):
        self.bot = bot
        self.cog_config = cog_config

    @commands.group(invoke_without_command=True)
    async def link(self, ctx):
        await ctx.send(f'{ctx.author.mention} use !help link for more information!')

    @link.command()
    async def epic(self, ctx, *, username):
        await ctx.send(f'{ctx.author.mention} your Epic account has been linked as ```{username}```')

    @link.command()
    async def steam(self, ctx, *, username):
        await ctx.send(f'{ctx.author.mention} your Steam account has been linked as ```{username}```')


def setup(bot):
    bot.add_cog(ConnectedAccounts(bot, bot.cog_config))
