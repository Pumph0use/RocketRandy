from discord.ext import commands


class UserManagement(commands.Cog):
    def __init__(self, bot, cog_config):
        self.bot = bot
        self.cog_config = cog_config

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Add user to database
        pass


def setup(bot):
    bot.add_cog(UserManagement(bot, bot.cog_config))
