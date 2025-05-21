from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    business_id = Column(Integer, ForeignKey("business_user.id"))
    business_email = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user_email = Column(String)
    message = Column(String)
    sender = Column(String)
    receiver = Column(String)
    timestamp = Column(DateTime, default=datetime.today)
    
    user = relationship("User", back_populates="chats")
