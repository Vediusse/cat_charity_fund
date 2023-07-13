from typing import List

import sqlalchemy as sq
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, ModelType
from app.models import CharityProject


class CharityCRUD(CRUDBase[CharityProject]):
    async def get_opened_projects(
        self, session: AsyncSession
    ) -> List[ModelType]:
        project = await session.execute(
            sq.select(self.model).where(self.model.fully_invested.is_(False))
        )
        return project.scalars().all()

    async def close_project(
        self, project_id: int, session: AsyncSession
    ) -> ModelType:
        project = await session.execute(
            sq.select(self.model).where(self.model.id == project_id)
        )
        project = project.scalars().first()
        project.fully_invested = True
        session.add(project)
        await session.commit()
        await session.refresh(project)

        return project


charity_crud = CharityCRUD(CharityProject)
