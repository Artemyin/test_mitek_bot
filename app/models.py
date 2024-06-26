from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db_conf import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class Voice(Base):
    __tablename__ = "voice"
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")


class Photo(Base):
    __tablename__ = "photo"
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
