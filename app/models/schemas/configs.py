from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"

    model_config = ConfigDict(from_attributes=True)


class ConfigOut(BaseResponse):
    min_withdraw: int
    exchange_rate: int
    task_price: float
    referral_percentage: int
    traffy_reward: int
    flyer_reward: int
    adsgram_video_reward: int
    adsgram_task_reward: int