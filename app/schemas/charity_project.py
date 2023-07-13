from typing import Optional

from pydantic import Field, BaseModel, Extra

from .base import BaseProjectSchema


class CharityDB(BaseProjectSchema):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(...)


class CharityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., ge=1)

    class Config:
        orm_mode = True


class CharityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, ge=1)

    class Config:
        orm_mode = True
        extra = Extra.forbid
