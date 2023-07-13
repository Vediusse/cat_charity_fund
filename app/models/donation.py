from sqlalchemy import Column, Text, ForeignKey, Integer

from app.models.base import BaseProjectModel


class Donation(BaseProjectModel):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text, default=None)
