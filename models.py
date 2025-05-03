from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_reply = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
