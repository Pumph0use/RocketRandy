import discord
import os
from discord.ext import commands
import json


def check_database():
    if not os.path.exists(f"tmp/wallets.json"):
        with open(f"tmp/wallets.json", "w") as out_file:
            wallets = {"wallets": []}
            json.dump(wallets, out_file)


class WalletManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        check_database()
        with open(f"tmp/wallets.json", "r") as in_file:
            self.data = json.load(in_file)

    @commands.group(invoke_without_command=True)
    async def wallet(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        member_wallet = self.get_wallet(member)
        await ctx.send(
            f"{member.mention} You have {member_wallet['contents']['basic_currency']} credits"
        )

    @wallet.command()
    @commands.is_owner()
    async def test_add(self, ctx, amount: int, member: discord.Member = None):
        member = member or ctx.author
        member_wallet = self.get_wallet(member)
        member_wallet["contents"]["basic_currency"] += amount
        with open(f"tmp/wallets.json", "w") as out_file:
            json.dump(self.data, out_file)
        await ctx.send(
            f"Your wallet has been updated to {member_wallet['contents']['basic_currency']}"
        )

    @wallet.command()
    @commands.is_owner()
    async def test_subtract(self, ctx, amount: int, member: discord.Member = None):
        member = member or ctx.author
        member_wallet = self.get_wallet(member)
        member_wallet["contents"]["basic_currency"] -= amount
        if member_wallet["contents"]["basic_currency"] < 0:
            member_wallet["contents"]["basic_currency"] = 0
        with open(f"tmp/wallets.json", "w") as out_file:
            json.dump(self.data, out_file)
        await ctx.send(
            f"Your wallet has been updated to {member_wallet['contents']['basic_currency']}"
        )

    def get_wallet(self, member: discord.Member):
        for wallet in self.data["wallets"]:
            if member.id == wallet["member_id"]:
                return wallet
        return self.add_wallet(member)

    def add_wallet(self, member: discord.Member):
        member_wallet = {"member_id": member.id, "contents": {"basic_currency": 1000}}
        self.data["wallets"].append(member_wallet)
        with open(f"tmp/wallets.json", "w") as out_file:
            json.dump(self.data, out_file, indent=4)

        return member_wallet


def setup(bot):
    bot.add_cog(WalletManager(bot))
