from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy.orm import validates

FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(
    timespec="minutes"
)

TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec="minutes")


class BaseProjectSchema(BaseModel):
    id: int
    full_amount: int = Field(..., ge=0)
    invested_amount: int = Field(..., ge=0)
    fully_invested: bool
    create_date: datetime = Field(..., example=FROM_TIME)
    close_date: Optional[datetime] = Field(
        ..., example=None, extra={"readOnly": True}
    )

    @validates("full_amount")
    def validate_full_amount(self, key, full_amount):
        if full_amount < self.invested_amount:
            raise ValueError(
                "Нельзя установить требуемую сумму меньше уже вложенной"
            )
        return full_amount

    class Config:
        orm_mode = True
