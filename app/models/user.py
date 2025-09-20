from sqlalchemy import Column, String, DateTime, BigInteger, Numeric
from sqlalchemy.dialects.postgresql import ARRAY
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
    ref = Column(String, nullable=True)
    ref_code = Column(String)
    ref_income = Column(BigInteger, default=0)
    ads_count = Column(BigInteger, default=0)
    tasks_completed = Column(ARRAY(String), default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tasks = relationship(
        "Task",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def __init__(
                    self, 
                    user_id: int,
                    ref_code: str,
                    ref: str = None,
                    username: str = None, 
                    lang: str = None,
                    full_name: str = None
                 ):
        self.user_id = user_id
        self.ref_code = ref_code
        self.ref = ref
        self.username = username
        self.lang = lang
        self.full_name = full_name

    def __repr__(self):
        return f"<User(id={self.user_id}, username={self.username})>"