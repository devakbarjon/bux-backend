from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from .base import BaseResponse


class BaseUserInput(BaseModel):
    init_data: str = Field(..., description="Initialization data for authentication")
    start_param: str = Field("", description="Start param from tg")


class UserOut(BaseResponse):
    user_id: int
    lang: Optional[str] = "ru"
    balance: int
    adv_balance: float
    ref_code: str
    ref_income: int
    ref_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)


class UserWithdrawIn(BaseModel):
    init_data: str = Field(..., description="Initialization data for authentication")
    wallet: str = Field(..., description="Address of ton wallet")


class UserWithdrawOut(BaseResponse):
    new_balance: int = Field(..., description="User's new balance.")


class UserLangIn(BaseModel):
    init_data: str = Field(..., description="Initialization data for authentication")
    lang: str = Field(..., description="New language code")  # e.g., 'en', 'ru'