from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Detection(Base):
    __tablename__ = "detections"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    object_class = Column(String)
    confidence = Column(Float)
