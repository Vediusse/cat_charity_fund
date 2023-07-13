from datetime import datetime

from pydantic import Field, BaseModel
from typing import Optional
from .base import BaseProjectSchema


class DonationsDB(BaseProjectSchema):
    user_id: int = Field(..., extra={"readOnly": True})
    comment: Optional[str] = ""


class DonationsCreate(BaseModel):
    comment: Optional[str] = None
    full_amount: int = Field(..., ge=1)


class DonationsUserView(DonationsCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
