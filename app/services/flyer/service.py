from flyerapi import Flyer
from app.core.config import settings


class FlyerService:
    def __init__(self):
        self.flyer = Flyer(key=settings.flyer_api_key)

    async def get_tasks(self, user_id: int | str, language_code: str = None):
        all_tasks = await self.flyer.get_tasks(
            user_id=user_id,
            language_code=language_code
        )

        sorted_tasks = []
        
        if all_tasks is not None:
            for task in all_tasks:
                if task["task"] == "subscribe channel":
                    sorted_tasks.append({
                        "id": task["signature"],
                        "title": task["name"] or "default",
                        "link": task["link"],
                        "reward": 10,
                        "type": "flyer_sub",
                    })

        return sorted_tasks
    
    async def check_task(self, user_id: int | str, signature: str):
        return await self.flyer.check_task(
            user_id=user_id,
            signature=signature
        )
    
FlyerServices = FlyerService()