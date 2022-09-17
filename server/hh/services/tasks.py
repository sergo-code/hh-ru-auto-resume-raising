from typing import (
    List,
    Optional,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .. import (
    models,
    tables,
)
from ..database import get_session


class TasksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self, user_id: int) -> List[tables.Tasks]:
        operations = (
            self.session
            .query(tables.Tasks)
            .filter(tables.Tasks.owner == user_id)
            .order_by(
                tables.Tasks.id.desc(),
            )
            .all()
        )
        return operations

    def create(
        self,
        user_id: int,
        operation_data: models.TasksCreate,
    ) -> tables.Tasks:
        operation = tables.Tasks(
            **operation_data.dict(),
            owner=user_id,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(
        self,
        user_id: int,
        operation_id: int,
        operation_data: models.TasksUpdate,
    ) -> tables.Tasks:
        operation = self._get(user_id, operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(
        self,
        user_id: int,
        operation_id: int,
    ):
        operation = self._get(user_id, operation_id)
        self.session.delete(operation)
        self.session.commit()

    def _get(self, user_id: int, operation_id: int) -> Optional[tables.Tasks]:
        operation = (
            self.session
            .query(tables.Tasks)
            .filter(
                tables.Tasks.owner == user_id,
                tables.Tasks.id == operation_id,
            )
            .first()
        )
        if not operation:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return operation
