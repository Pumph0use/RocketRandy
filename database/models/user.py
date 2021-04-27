import discord

from database import Base
from sqlalchemy import Column, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    member_id = Column(BigInteger, primary_key=True, autoincrement=False)
    date_first_seen = Column(DateTime, default=datetime.utcnow())
    display_name = Column(String)

    rl_threes_ranks = relationship('RLThreesRank', back_populates='user')

    def __init__(self, member: discord.Member):
        self.member_id = member.id
        self.display_name = member.display_name
