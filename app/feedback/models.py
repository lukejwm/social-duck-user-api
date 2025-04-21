from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from app.database import Base

class BusinessUser(Base):
    __tablename__ = "business_user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    business_name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    town_city = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    username = Column(String(100), nullable=False)
    business_id = Column(Integer, ForeignKey("business_user.id"), nullable=False)
    business_name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    title = Column(String(75), nullable=False)
    body = Column(Text, nullable=False)
    photo_filename = Column(String(255), nullable=True)
    star_rating = Column(TINYINT(unsigned=True), nullable=False)
    review_type = Column(Enum("Positive", "Negative"), nullable=False)