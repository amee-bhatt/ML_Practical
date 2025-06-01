from typing import Optional

from pydantic import EmailStr, BaseModel
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field


class RegisterOrganization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_name: str
    owner_name: str = Field(default="Admin")
    email: EmailStr = Field(
        sa_column=Column("email", String, unique=True, nullable=False)
    )


class OrgCreate(BaseModel):
    org_name: str
    owner_name: str
    email: EmailStr
class OrgGetRequest(BaseModel):
    organization_name: str