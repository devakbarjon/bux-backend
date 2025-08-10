from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"


class BaseUserInput(BaseModel):
    init_data: str = Field(..., description="Initialization data for authentication")
    start_param: str = Field("", description="Start param from tg")


class UserOut(BaseResponse):
    user_id: int
    lang: Optional[str] = "en"
    balance: int
    adv_balance: float

    model_config = ConfigDict(from_attributes=True)


class UserWithdrawIn(BaseModel):
    init_data: str = Field(..., description="Initialization data for authentication")
    wallet: str = Field(..., description="Address of ton wallet")


class UserWithdrawOut(BaseResponse):
    new_balance: int = Field(..., description="User's new balance.")