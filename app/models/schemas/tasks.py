from pydantic import BaseModel, Field, ConfigDict


class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"

    model_config = ConfigDict(from_attributes=True)


class TaskInput(BaseModel):
    init_data: str = Field(..., description="Initialization data for authentication")
    task_id: int = Field(..., description="Id of specific tasks")


class TaskOut(BaseResponse):
    id: int
    title: str
    link: str
    reward: int
    type: str


class TaskListOut(BaseModel):
    id: int
    title: str
    link: str
    reward: int
    type: str

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseResponse):
    tasks: list[TaskListOut]


class AddTaskIn(BaseModel):
    init_data: str = Field(..., description="Initialization data for authentication")
    link: str = Field("https://t.me/ton_bux_bot", description="Link to task resource")
    check_sub: bool = Field(..., description="Is resource should be checked")
    count: int = Field(..., description="Count of completion")

class CheckTaskOut(BaseResponse):
    task_id: int
    new_balance: int