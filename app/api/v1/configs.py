from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.configs import get_config
from app.models.schemas.configs import ConfigOut

router = APIRouter()


@router.get("/", response_model=ConfigOut)
async def get_configs(session: AsyncSession = Depends(get_db)):
    config = await get_config(session=session)

    if not config:
        raise HTTPException(status_code=400, detail="Configs are not set yet.")

    return ConfigOut.from_orm(config)