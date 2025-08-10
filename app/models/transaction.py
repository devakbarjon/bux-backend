from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    amount = Column(Numeric(precision=20, scale=4), nullable=False)
    status = Column(String, default='pending')  # 'pending', 'completed', 'failed'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="transactions")

    def __init__(self, user_id: int, amount: float, status: str, transaction_id: str = None):
        self.user_id = user_id
        self.amount = amount
        self.status = status
        self.transaction_id = transaction_id

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, status={self.status})>"
