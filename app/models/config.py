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
    referral_percentage = Column(Integer, default=5)
    traffy_reward = Column(Integer, default=10)
    flyer_reward = Column(Integer, default=10)
    adsgram_video_reward = Column(Integer, default=10)
    adsgram_task_reward = Column(Integer, default=10)