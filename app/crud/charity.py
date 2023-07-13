from app.crud.base import CRUDBase
from app.models import CharityProject

charity_crud = CRUDBase[CharityProject](CharityProject)
