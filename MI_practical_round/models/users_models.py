from typing import Optional

from pydantic import EmailStr, BaseModel
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(
        sa_column=Column("email", String, unique=True, nullable=False)
    )
    password: str
    is_admin: bool = Field(default=False)
    otp: Optional[str] = Field(default=None)


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    token: str
    email: str
    org: str


class CreateUserWithTokenRequest(BaseModel):
    token: str
    email: EmailStr
    password: str
