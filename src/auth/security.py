from typing import Optional

import jwt
from fastapi import HTTPException
from starlette import status
from starlette.requests import Request

import settings
from auth.schemas import TokenUserPayload


def get_user(request: Request) -> TokenUserPayload:
    """
    Protect route from anonymous access, requiring and returning current
    authenticated user.

    :param request: web request
    :return: current user, otherwise raise an HTTPException (status=401)
    """

    return _check_and_extract_user(request)


def get_admin(request: Request) -> TokenUserPayload:
    """
    Allow access only to an 'admin' account, returning current
    authenticated admin account data.

    :param request: web request
    :return: current admin user, otherwise raise an HTTPException (status=401)
    """

    user = _check_and_extract_user(request)
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


def get_optional_user(request: Request) -> Optional[TokenUserPayload]:
    """
    Return authenticated user or None if session is anonymous.

    :param request: web request
    :return: current user or None for anonymous sessions
    """
    try:
        return _check_and_extract_user(request)
    except HTTPException:
        if request.headers.get("Authorization"):
            raise


def extract_user_from_token(access_token: str) -> TokenUserPayload:
    """
    Extract User object from jwt token, with optional expiration check.

    :param access_token: encoded access token string
    :param verify_exp: whether to perform verification or not
    :return: User object stored inside the jwt
    """

    return TokenUserPayload(
        **jwt.decode(
            access_token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        ).get("user")
    )


def _check_and_extract_user(request: Request) -> TokenUserPayload:
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        access_token = authorization_header.replace("Bearer ", "")
        token_user_payload = extract_user_from_token(access_token)

        return token_user_payload
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
