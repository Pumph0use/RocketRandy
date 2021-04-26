import discord

from database.models import Base
from sqlalchemy import Column, Integer, String, Date, BigInteger
from datetime import date


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_member_id = Column(BigInteger)
    date_joined = Column(Date)
    display_name = Column(String)

    def __init__(self, member: discord.Member):
        self.discord_member_id = member.id
        self.date_joined = date.today()
        self.display_name = member.display_name

