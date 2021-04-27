from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship


class GreetingResponse(Base):
    __tablename__ = "greetings"

    id = Column(Integer, primary_key=True)
    response = Column(String)

    def __init__(self, response):
        self.response = response

