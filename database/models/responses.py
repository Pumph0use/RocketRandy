from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship


class GreetingResponse(Base):
    __tablename__ = "greetings"

    id = Column(Integer, primary_key=True)
    response = Column(String)
    added_by = Column(BigInteger, ForeignKey("users.member_id"))

    def __init__(self, response, member_id):
        self.response = response
        self.member_id = member_id
