from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityUpdate


async def charity_name_duplicate(
    name: str,
    session: AsyncSession,
) -> None:
    charity = await charity_crud.get_by_attribute("name", name, session)
    if charity is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


async def charity_exists(
    charity_id: int,
    session: AsyncSession,
) -> None:
    charity = await charity_crud.get(charity_id, session)
    if charity is None:
        raise HTTPException(status_code=404, detail="Проект не найдена!")


async def charity_possible_to_change(
    charity_id: int, session: AsyncSession, update_value: CharityUpdate
) -> CharityProject:
    charity = await charity_crud.get(charity_id, session)
    if charity is None:
        raise HTTPException(status_code=404, detail="Проект не найдена!")

    if (
        update_value.full_amount is not None and
        charity.invested_amount > update_value.full_amount
    ):
        raise HTTPException(
            status_code=422,
            detail="Нельзя установить требуемую сумму меньше уже вложенной.",
        )

    if charity.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail="Закрытый проект нельзя редактировать!",
        )

    return charity


async def charity_possible_to_delete(
    charity_id: int,
    session: AsyncSession,
) -> None:
    charity = await charity_crud.get(charity_id, session)
    if charity.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )

    if charity.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить закрытый проект!",
        )
