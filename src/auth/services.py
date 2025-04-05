import datetime

import bcrypt
import jwt
from dependency_injector.wiring import Provide
from fastapi import HTTPException
from starlette import status

from auth.exceptions import LoginFailed
from auth.schemas import LoggedInUser, LoginRequest, TokenUserPayload
from users.services import UserService
from utils.utils import cpu_bound_task


class AuthService:

    def __init__(self, user_service: UserService = Provide["user_service"]):
        self.user_service = user_service

    async def login(self, lreq: LoginRequest):
        try:
            user = await self.user_service.get_user_by_email(str(lreq.email))
            if not user or not await self._check_password(lreq.password, user.password):
                raise LoginFailed()
            access_token = self._generate_jwt_access_token(LoggedInUser(user))
        except LoginFailed:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"access_token": access_token}

    async def _check_password(self, password: str, password_hash: str) -> bool:
        return await cpu_bound_task(
            bcrypt.checkpw, password.encode(), password_hash.encode()
        )

    def _generate_jwt_access_token(self, user_data: LoggedInUser) -> str:
        iat = datetime.datetime.now(datetime.timezone.utc)
        permissions = None
        if user_data.role and user_data.role.permissions:
            permissions = [permission.name for permission in user_data.role.permissions]

        user_payload = TokenUserPayload(
            id=user_data.id,
            email=user_data.email,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
            is_admin=user_data.is_admin,
            role=user_data.role.name if user_data.role else None,
            permissions=permissions,
        )
        payload = dict(iat=iat, user=user_payload.model_dump())
        enc_jwt = jwt.encode(payload=payload, key="secret", algorithm="HS256")
        return enc_jwt
