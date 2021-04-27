import discord

from database import Base
from sqlalchemy import Column, String, Date, BigInteger
from datetime import date


class User(Base):
    __tablename__ = "users"

    member_id = Column(BigInteger, primary_key=True, autoincrement=False)
    date_first_seen = Column(Date)
    display_name = Column(String)

    def __init__(self, member: discord.Member):
        self.member_id = member.id
        self.date_first_seen = date.today()
        self.display_name = member.display_name
