import enum

import discord

from database import Base
from sqlalchemy import Column, String, DateTime, BigInteger, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Platforms(enum.Enum):
    steam = 1
    epic = 2


class User(Base):
    __tablename__ = "users"

    member_id = Column(BigInteger, primary_key=True, autoincrement=False)
    date_first_seen = Column(DateTime, default=datetime.utcnow())
    display_name = Column(String(32))

    rl_threes_ranks = relationship("RLThreesRank", back_populates="user")
    connected_accounts = relationship("ConnectedAccount", back_populates="user")

    def __init__(self, member: discord.Member):
        self.member_id = member.id
        self.display_name = member.display_name


class ConnectedAccount(Base):
    __tablename__ = "connectedaccounts"

    id = Column(Integer, primary_key=True)
    member_id = Column(BigInteger, ForeignKey("users.member_id"))
    platform = Column(Enum(Platforms))
    platform_username = Column(String(32))

    user = relationship("User", back_populates="connected_accounts")

    def __init__(self, platform, username):
        self.platform_username = username
        self.platform = platform
