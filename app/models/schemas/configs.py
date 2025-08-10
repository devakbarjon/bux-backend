from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"

    model_config = ConfigDict(from_attributes=True)


class ConfigOut(BaseResponse):
    min_withdraw: int
    exchange_rate: int
    task_price: float