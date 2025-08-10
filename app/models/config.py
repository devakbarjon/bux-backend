from sqlalchemy import (
    Column, Integer, Numeric
)

from app.db.database import Base


class Config(Base):
    __tablename__ = 'configs'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    min_withdraw = Column(Integer, default=1000)
    exchange_rate = Column(Integer, default=100)
    task_price = Column(Numeric(precision=20, scale=4), default=0)