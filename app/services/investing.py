from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import donation_crud, charity_crud
from app.models import CharityProject, Donation


async def investing(session: AsyncSession):
    donations: List[Donation] = await donation_crud.get_vacant_donations(
        session
    )
    charities: List[CharityProject] = await charity_crud.get_opened_projects(
        session
    )
    charities_iter = iter(charities)

    try:
        charity = next(charities_iter)
    except StopIteration:
        return

    for donation in donations:
        free_amount = donation.full_amount - donation.invested_amount

        charity_amount = charity.full_amount - charity.invested_amount
        invested_amount = min(free_amount, charity_amount)
        charity.invested_amount += invested_amount
        donation.invested_amount += invested_amount

        donation.fully_invested = (
            donation.invested_amount == donation.full_amount
        )
        charity.fully_invested = (
            charity.invested_amount == charity.full_amount
        )
        if charity.fully_invested:
            charity.close_date = datetime.now()

        session.add(charity)
        session.add(donation)

        if not charity.fully_invested or not donations:
            break

        try:
            charity = next(charities_iter)
        except StopIteration:
            break

    await session.commit()

    for charity in charities:
        await session.refresh(charity)

    for donation in donations:
        await session.refresh(donation)
