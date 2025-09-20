from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_serializer
from .base import BaseResponse


class TransIn(BaseModel):
    init_data: str

class TransListOut(BaseModel):
    id: int
    transaction_id: str | None
    amount: float
    status: str
    type: str
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

    model_config = ConfigDict(from_attributes=True)


class TransListResponse(BaseResponse):
    transactions: list[TransListOut]