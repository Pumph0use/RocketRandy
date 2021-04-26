from database.models import Base
from sqlalchemy import Column, Integer, String, Date, BigInteger
from datetime import date


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_member_id = Column(BigInteger)
    date_joined = Column(Date)

    def __init__(self, discord_member_id):
        self.discord_member_id = discord_member_id
        self.date_joined = date.today()
