from typing import List

from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_crud
from app.schemas.charity_project import (
    CharityDB,
    CharityUpdate,
    CharityCreate,
)
from app.services.investing import investing

router = InferringRouter()


@cbv(router)
class CharityCBV:
    session: AsyncSession = Depends(get_async_session)

    @router.get(
        "/",
        response_model_exclude_none=True,
    )
    async def get_all(self) -> List[CharityDB]:
        all_charity = await charity_crud.get_opened_projects(self.session)
        return all_charity

    @router.post(
        "/",
        dependencies=[Depends(current_superuser)],
        response_model_exclude_none=True,
    )
    async def create(self, charity: CharityCreate) -> CharityDB:
        await validators.charity_name_duplicate(charity.name, session=self.session)
        charity = await charity_crud.create(charity, session=self.session)
        await investing(session=self.session)

        return charity

    @router.delete(
        "/{project_id}",
        dependencies=[Depends(current_superuser)],
    )
    async def delete(self, project_id: int) -> CharityDB:
        await validators.charity_exists(project_id, session=self.session)
        await validators.charity_possible_to_delete(project_id, session=self.session)
        charity = await charity_crud.delete(model_id=project_id, session=self.session)
        return charity

    @router.patch(
        "/{project_id}",
        dependencies=[Depends(current_superuser)],
    )
    async def update(self, project_id: int, charity_update: CharityUpdate) -> CharityDB:
        await validators.charity_name_duplicate(
            charity_update.name, session=self.session
        )
        charity = await validators.charity_possible_to_change(
            project_id, session=self.session, update_value=charity_update
        )
        charity = await charity_crud.update(
            db_obj=charity, obj_in=charity_update, session=self.session
        )
        if charity.invested_amount == charity.full_amount:
            await charity_crud.close_project(charity.id, session=self.session)

        return charity
