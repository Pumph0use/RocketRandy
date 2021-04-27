from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship


class GreetingResponse(Base):
    __tablename__ = "greetings"

    id = Column(Integer, primary_key=True)
    response = Column(String, unique=True)
    added_by = Column(BigInteger, ForeignKey("users.member_id"))

    user = relationship("User")

    def __init__(self, response, member_id):
        self.response = response
        self.added_by = member_id
