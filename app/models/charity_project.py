from sqlalchemy import Column

from app.models.base import BaseProjectModel


class CharityProject(BaseProjectModel):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
