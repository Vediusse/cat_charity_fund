import sqlalchemy as sq
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud.base import CRUDBase, ModelType
from app.models import Donation, User


class DonationCRUD(CRUDBase[Donation]):
    async def get_vacant_donations(self, session: AsyncSession) -> List[ModelType]:
        donations = await session.execute(
            sq.select(self.model).where(self.model.fully_invested.is_(False))
        )
        return donations.scalars().all()

    async def get_my_donations(self, user: User, session: AsyncSession):
        db_objs = await session.execute(
            sq.select(self.model).where(self.model.user_id == user.id)
        )
        return db_objs.scalars().all()


donation_crud = DonationCRUD(Donation)
