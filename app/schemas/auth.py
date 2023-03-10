from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: Optional[str] = None


class RegUser(BaseModel):
    name: str
    surname: str
    phone: str
    nickname: str


class AuthUser(BaseModel):
    nickname: str = Field(..., max_length=30)


class SuccessfulResponse(BaseModel):
    details: str = Field("Выполнено", title="Статус операции")


class UserInfo(BaseModel):
    name: str
    surname: str
    phone: str
    nickname: str
    role: str
