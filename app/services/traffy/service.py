import aiohttp
from typing import TypedDict, Union
from app.core.config import settings


BASE_URL = "https://api.traffy.site/v1"


class VerificationSuccess(TypedDict):
    success: bool
    data: dict


class VerificationFail(TypedDict):
    success: bool
    data: None


VerificationResponse = Union[VerificationSuccess, VerificationFail]


class TraffyService:
    def __init__(self, resource_id: str):
        self.resource_id = resource_id

    async def verify_signed_token(self, token: str) -> VerificationResponse:
        url = f"{BASE_URL}/mixer/app/verify_token"
        params = {"token": token}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                return await resp.json()


TraffyServices = TraffyService(resource_id=settings.traffy_resource_id)