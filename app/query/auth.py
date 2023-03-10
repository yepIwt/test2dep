from sqlalchemy import select
from app.db.models import Users
from app.schemas.auth import RegUser, UserInfo
from app.schemas.exception import UserFoundException, NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession


async def check_nickname(nickname: str, session: AsyncSession):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    if user:
        raise UserFoundException(error="Юзер с таким nickname существует")


async def create_user(new_user: RegUser, session: AsyncSession):
    new_user = Users(
        nickname=new_user.nickname,
        name=new_user.name,
        surname=new_user.surname,
        user_type="User",
        phone=new_user.phone,
    )
    session.add(new_user)
    await session.commit()


async def find_by_nickname(nickname: str, session: AsyncSession) -> str:
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    if not user:
        raise NotFoundException(error="Пользователь не найден")


async def get_info(nickname: str, session: AsyncSession):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    userOut = UserInfo(
        name=user.name,
        surname=user.surname,
        nickname=user.nickname,
        phone=user.phone,
        role=user.user_type
    )
    return userOut
