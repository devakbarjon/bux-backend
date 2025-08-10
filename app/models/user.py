from sqlalchemy import Column, String, DateTime, BigInteger, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True, unique=True)
    full_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    lang = Column(String, nullable=True)
    balance = Column(BigInteger, default=0)
    adv_balance = Column(Numeric(precision=20, scale=4), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tasks = relationship(
        "Task",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, 
                 user_id: int, 
                 username: str = None, 
                 lang: str = None
                 ):
        self.user_id = user_id
        self.username = username
        self.lang = lang

    def __repr__(self):
        return f"<User(id={self.user_id}, username={self.username})>"