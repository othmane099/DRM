from fastapi import HTTPException
from starlette import status

from auth.schemas import TokenUserPayload


def is_authorized(user: TokenUserPayload, *permissions: str) -> bool:
    if user.is_superuser or user.is_admin:
        return True

    if not permissions:
        is_valid = False
    else:
        is_valid = any(perm in user.permissions for perm in permissions)

    if not is_valid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return is_valid
