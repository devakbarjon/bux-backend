from flyerapi import Flyer
from app.core.config import settings


class FlyerService:
    def __init__(self):
        self.flyer = Flyer(api_key=settings.flyer_api_key)

    async def get_tasks(self, user_id: int | str, language_code: str = None):
        return await self.flyer.get_tasks(
            user_id=user_id,
            language_code=language_code
        )
    
    async def check_task(self, user_id: int | str, signature: str):
        return await self.flyer.check_task(
            user_id=user_id,
            signature=signature
        )
    
FlyerServices = FlyerService()