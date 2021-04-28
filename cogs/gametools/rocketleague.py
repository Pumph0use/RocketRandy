import logging
import math
import os
import json

import discord
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv
from database import Session
from database.models.rocketleague import RLThreesRank, RLTwosRank, RLOnesRank
from database.models import User, ConnectedAccount
from database.models.user import Platforms

load_dotenv()
RL_TRACKER_URL = os.getenv("RL_TRACKER_URL")


async def write_response_to_file(ctx, response, platform, username, file_name):
    out_dir = f"tmp/{platform}/{username}"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out_file = os.path.join(out_dir, f"{file_name}.json")
    with open(out_file, "w") as out_data:
        json.dump(response, out_data, indent=4)
    await ctx.send(
        f"{ctx.author.mention} here is your requested data!",
        file=discord.File(out_file),
    )


async def log_request_error(ctx, request):
    logging.info(f"Received {request.status} from Tracker Network!!!")
    await ctx.send(
        f"I'm so sorry {ctx.author.mention}. "
        f"I am having trouble communicating with my contacts on the inside. "
        f"Please try again later. If the problem persists, contact the server owner."
    )
    return None


class RocketLeague(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.command()
    @commands.is_owner()
    async def set_role(
        self, ctx, platform: str, username: str, member: discord.Member = None
    ):
        member = member or ctx.author

        results = await self.get_user_info(ctx, platform, username)

        if results:
            if results["data"]:
                self.logger.info(f"Found data for {username}...")
                if results["data"]["segments"]:
                    self.logger.info(f"Found playlist data for {username}...")
                    max_mmr = -math.inf
                    best_playlist_id = 0
                    best_playlist_name = None
                    for segment in results["data"]["segments"]:
                        if segment["type"] == "playlist":
                            if segment["attributes"]["playlistId"] in [10, 11, 13]:
                                playlist_mmr = segment["stats"]["rating"]["value"]
                                if playlist_mmr > max_mmr:
                                    max_mmr = playlist_mmr
                                    best_playlist_id = segment["attributes"][
                                        "playlistId"
                                    ]
                                    best_playlist_name = segment["metadata"]["name"]
                                    best_rank = segment["stats"]["tier"]["metadata"][
                                        "name"
                                    ]

                    if best_rank not in [role.name for role in ctx.guild.roles]:
                        self.logger.info(f"Creating role {best_rank}...")
                        new_role = await ctx.guild.create_role(
                            name=best_rank, mentionable=True
                        )
                        await member.add_roles(new_role)
                    else:
                        for role in ctx.guild.roles:
                            if role.name == best_rank:
                                if member not in role.members:
                                    self.logger.info(
                                        f"Adding {member.name} to {role.name}..."
                                    )
                                    await member.add_roles(role)

                    await ctx.send(
                        f"{member.mention} Your best playlist ID is "
                        f"(ID: {best_playlist_id}) {best_playlist_name}, "
                        f"and you have been assigned the rank role of {best_rank}"
                    )
            else:
                await ctx.send(
                    f"{member}, I'm truly sorry sir/madam, "
                    f"my contacts don't seem to have any information on you. You are quite sneaky."
                )

    # region !rl

    @commands.group(invoke_without_command=True)
    async def rl(self, ctx):
        await ctx.send(
            f"{ctx.author.mention} please try !help for information on things I can do."
        )

    @rl.command()
    async def sessions(
        self, ctx, platform: str, username: str, member: discord.Member = None
    ):
        member = member or ctx.author

        response = await self.get_user_sessions(ctx, platform, username)

        if response:
            await write_response_to_file(ctx, response, platform, username, "sessions")

    # region !mmr

    @rl.group(invoke_without_command=True)
    async def mmr(
        self, ctx, platform: str, username: str, member: discord.Member = None
    ):
        member = member or ctx.author

        response = await self.get_user_info(ctx, platform, username)

        if response["data"]:
            self.logger.info(f"Found data for {username}...")
            if response["data"]["segments"]:
                self.logger.info(f"Found playlist data for {username}...")
                max_mmr = -math.inf
                best_playlist_id = 0
                best_playlist_name = None
                for segment in response["data"]["segments"]:
                    if segment["type"] == "playlist":
                        cur_playlist_id = segment["attributes"]["playlistId"]
                        # 11 2's
                        # 10 1's
                        if cur_playlist_id in [10, 11, 13]:
                            playlist_mmr = segment["stats"]["rating"]["value"]
                            if playlist_mmr > max_mmr:
                                max_mmr = playlist_mmr
                                best_playlist_id = segment["attributes"]["playlistId"]
                                best_playlist_name = segment["metadata"]["name"]
                                best_rank = segment["stats"]["tier"]["metadata"]["name"]

                await ctx.send(
                    f"{member.mention} Your best playlist is "
                    f"(ID: {best_playlist_id}) {best_playlist_name}, "
                    f"and your MMR is {max_mmr}"
                )

    @mmr.command()
    async def dl(
        self, ctx, platform: str, username: str, member: discord.Member = None
    ):
        member = member or ctx.author

        response = await self.get_user_info(ctx, platform, username)

        if response:
            await write_response_to_file(ctx, response, platform, username, "segments")

    @mmr.command()
    async def threes(
        self, ctx, platform: str, username: str, member: discord.Member = None
    ):
        member = member or ctx.author
        response = await self.get_user_info(ctx, platform, username)

        threes, twos, ones = await self.extract_rocket_league_data(
            ctx, member, platform, response, username
        )
        await ctx.send(f"{member.mention} Your 3v3 mmr is {threes}")

    @mmr.command()
    async def twos(
        self, ctx, platform: str, username: str, member: discord.Member = None
    ):
        member = member or ctx.author
        response = await self.get_user_info(ctx, platform, username)
        threes, twos, ones = await self.extract_rocket_league_data(
            ctx, member, platform, response, username
        )
        await ctx.send(f"{member.mention} Your 2v2 mmr is {twos}")

    @mmr.command()
    async def ones(
        self, ctx, platform: str, username: str, member: discord.Member = None
    ):
        member = member or ctx.author
        response = await self.get_user_info(ctx, platform, username)
        threes, twos, ones = await self.extract_rocket_league_data(
            ctx, member, platform, response, username
        )
        await ctx.send(f"{member.mention} Your 1v1 mmr is {ones}")

    async def extract_rocket_league_data(self, ctx, member, platform, response, username):
        if response["data"]:
            self.logger.info(f"Found data for {username}...")
            cur_platform = None

            platform = 'psn' if platform.lower() in ['ps4', 'ps5', 'playstation', 'ps3', 'ps2', 'ps1'] else platform

            if platform == 'psn':
                cur_platform = Platforms.psn
            elif platform == 'steam':
                cur_platform = Platforms.steam
            elif platform == 'epic':
                cur_platform = Platforms.epic

            if cur_platform is None:
                await ctx.send(f'{ctx.author.mention} You must provide a valid platform!')
                return None, None, None

            session = Session()
            user = session.query(User).filter(User.member_id == member.id).first()
            new_user = False
            if user:
                already_connected = False
                for account in user.connected_accounts:
                    already_connected = account.platform == cur_platform

                if not already_connected:
                    user.connected_accounts.append(
                        ConnectedAccount(cur_platform, username)
                    )
            else:
                new_user = True
                user = User(member)
                user.connected_accounts.append(ConnectedAccount(cur_platform, username))

            rl_threes_rank = None
            rl_twos_rank = None
            rl_ones_rank = None

            if response["data"]["segments"]:
                self.logger.info(f"Found playlist data for {username}...")
                for segment in response["data"]["segments"]:
                    if segment["type"] == "playlist":
                        cur_playlist_id = segment["attributes"]["playlistId"]
                        playlist_mmr = segment["stats"]["rating"]["value"]
                        season = segment["attributes"]["season"]
                        if cur_playlist_id == 13:
                            # 13 3's
                            rl_threes_rank = RLThreesRank(season, playlist_mmr)
                            rl_threes_rank.user = user
                        elif cur_playlist_id == 11:
                            # 11 2's
                            rl_twos_rank = RLTwosRank(season, playlist_mmr)
                            rl_twos_rank.user = user
                        elif cur_playlist_id == 10:
                            # 10 1's
                            rl_ones_rank = RLOnesRank(season, playlist_mmr)
                            rl_ones_rank.user = user

            if new_user:
                session.add(user)

            threes_mmr = rl_threes_rank.mmr
            twos_mmr = rl_twos_rank.mmr
            ones_mmr = rl_ones_rank.mmr
            session.commit()

            return threes_mmr, twos_mmr, ones_mmr

    # endregion

    # endregion

    async def get_user_info(self, ctx, platform: str, username: str):
        self.logger.info(f"Looking on {platform} for user {username}...")
        platform = platform.lower()
        username = username.strip("\"'").replace(" ", "%20")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{RL_TRACKER_URL}/standard/profile/{platform}/{username}"
            ) as request:
                if request.status == 200:
                    return await request.json()
                else:
                    return await log_request_error(ctx, request)

    async def get_user_sessions(self, ctx, platform: str, username: str):
        self.logger.info(f"Getting sessions for user {username} on platform {platform}")
        platform = platform.lower()
        username = username.strip("\"'").replace(" ", "%20")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{RL_TRACKER_URL}/standard/profile/{platform}/{username}/sessions"
            ) as request:
                if request.status == 200:
                    return await request.json()
                else:
                    return await log_request_error(ctx, request)


def setup(bot):
    bot.add_cog(RocketLeague(bot))
