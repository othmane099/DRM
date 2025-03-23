from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from auth.schemas import LoginRequest
from auth.services import AuthService

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/login")
@inject
async def login(
    req: LoginRequest, auth_service: AuthService = Depends(Provide["auth_service"])
):
    response = await auth_service.login(req)
    return response
