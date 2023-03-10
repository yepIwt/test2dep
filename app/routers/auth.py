from datetime import timedelta

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.schemas.auth import Token, RegUser, AuthUser, UserInfo
from app.config import auth
from app.auth.jwttoken import create_access_token
from app.query.auth import check_nickname, create_user, find_by_nickname, get_info
from app.auth.oauth2 import get_current_user
from app.IIko import get_token_iiko


registr_router = APIRouter(tags=["Authorization"])


@registr_router.post(
    "/registration", response_model=Token, status_code=status.HTTP_200_OK
)
async def registration_user(
    new_user: RegUser = Body(...), session: AsyncSession = Depends(get_session)
) -> Token:
    await check_nickname(new_user.nickname, session)
    await create_user(new_user, session)
    # generate a jwt token and return
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.nickname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@registr_router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    nickname: AuthUser = Body(...), session: AsyncSession = Depends(get_session)
) -> Token:
    await find_by_nickname(nickname.nickname, session)
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": nickname.nickname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@registr_router.get("/whoiam", response_model=UserInfo, status_code=status.HTTP_200_OK)
async def get_info_user(
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
    token: str = Depends(get_token_iiko)
):
    print(token)
    return await get_info(current_user, session)
