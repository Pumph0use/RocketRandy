import datetime

from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime


class RLThreesRank(Base):
    __tablename__ = 'rlthreesranks'

    id = Column(Integer, primary_key=True)
    member_id = Column(BigInteger, ForeignKey('users.member_id'))
    season = Column(Integer)
    mmr = Column(Integer)
    date_collected = Column(DateTime, default=datetime.utcnow())

    user = relationship('User', back_populates='rl_threes_ranks')

    def __init__(self, season, mmr):
        self.season = season
        self.mmr = mmr