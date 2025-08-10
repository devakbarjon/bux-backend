from sqlalchemy import (
    Column, ForeignKey, Text, BigInteger, Boolean, Integer,
    DateTime, func
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.db.database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    status = Column(Boolean, default=True)
    link = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    reward = Column(BigInteger, default=100)
    type = Column(Text, nullable=False)
    check_sub = Column(Boolean, default=False)
    users = Column(ARRAY(BigInteger), default=list)

    end_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="tasks")

    def __init__(self, user_id, link, title, reward, type, check_sub):
        self.user_id = user_id
        self.title = title
        self.link = link
        self.reward = reward
        self.type = type
        self.check_sub = check_sub

    def __repr__(self):
        return f"<Task(id={self.id}, user_id={self.user_id})>"
