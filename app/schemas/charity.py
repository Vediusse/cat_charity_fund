from typing import Optional

from pydantic import Field, BaseModel

from .base import BaseProjectSchema


class CharityDB(BaseProjectSchema):
    name: str = Field(..., min_length=0, max_length=100)
    description: str = Field(...)


class CharityCreate(BaseModel):
    name: str = Field(..., min_length=0, max_length=100)
    description: str
    full_amount: int = Field(..., ge=1)


class CharityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=0, max_length=100)
    description: Optional[str]
    full_amount: Optional[int] = Field(None, ge=1)
