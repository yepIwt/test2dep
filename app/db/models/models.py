# pylint: disable=R0903
from sqlalchemy import CheckConstraint, Column, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import (
    BOOLEAN,
    CHAR,
    INTEGER,
    JSONB,
    TIMESTAMP,
    VARCHAR,
    FLOAT,
    UUID,
    TEXT
)
from sqlalchemy.types import DateTime as sqlalchemy_DateTime
import uuid
from sqlalchemy.orm import declarative_base
from enum import Enum
from app.db import convention


metadata = MetaData(naming_convention=convention)
DeclarativeBase = declarative_base(metadata=metadata)


class User_type(Enum):
    Admin = 1
    User = 2


class Users(DeclarativeBase):
    __tablename__ = "users"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    nickname = Column("nickname", VARCHAR(30), nullable=False)
    name = Column("name", VARCHAR(15), nullable=False)
    user_type = Column("user_type", VARCHAR(15), nullable=False)
    surname = Column("surname", VARCHAR(20), nullable=False)
    phone = Column("phone", CHAR(12), nullable=False)


class Roulette(DeclarativeBase):

    __tablename__ = "roulette"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column("title", TEXT, nullable=False)

    start = Column("start", sqlalchemy_DateTime(timezone=True), nullable=False)
    end = Column("end", sqlalchemy_DateTime(timezone=True), nullable=False)
    score = Column("score", INTEGER, nullable=False)
    winners_count = Column("winners_count", INTEGER, nullable=False)


class UserRoulette(DeclarativeBase):
    
    __tablename__ = "userroulette"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(
        "user_id",
        UUID,
        ForeignKey(Users.id, ondelete="CASCADE"),
        nullable=False,
    )

    roulette_id = Column(
        "roulette_id",
        UUID,
        ForeignKey(Roulette.id, ondelete="CASCADE"),
        nullable=False,
    )

    is_winner = Column(
        "is_winner",
        BOOLEAN,
        nullable=True,
    )