from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationsDB,
    DonationsUserView,
    DonationsCreate,
)
from app.services.investing import investing

router = InferringRouter()


@cbv(router)
class DonationCBV:
    session: AsyncSession = Depends(get_async_session)

    @router.get(
        "/",
        dependencies=[Depends(current_superuser)],
        response_model_exclude_none=True,
    )
    async def get_all(self) -> List[DonationsDB]:
        donations = await donation_crud.get_multi(session=self.session)
        return donations

    @router.post(
        "/",
        response_model_exclude_none=True,
    )
    async def create(
        self, donation: DonationsCreate, user: User = Depends(current_user)
    ) -> DonationsUserView:
        donation = await donation_crud.create(
            obj_in=donation, user=user, session=self.session
        )
        await investing(session=self.session)
        return donation

    @router.get("/my")
    async def get_my(
        self, user: User = Depends(current_user)
    ) -> List[DonationsUserView]:
        donations = await donation_crud.get_my_donations(
            user=user, session=self.session
        )
        return donations
