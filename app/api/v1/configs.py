from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.configs import get_config
from app.models.schemas.configs import ConfigOut
from app.models.schemas.errors import ErrorResponse

router = APIRouter()


@router.get("/", response_model=ConfigOut | ErrorResponse)
async def get_configs(session: AsyncSession = Depends(get_db)):
    config = await get_config(session=session)

    if not config:
        return ErrorResponse(
            code="config_not_found",
            message="The requested configuration does not exist."
        )

    return ConfigOut.from_orm(config)