from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from .. import models
from ..services.auth import get_current_user
from ..services.tasks import TasksService


router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)


@router.get(
    '/',
    response_model=List[models.Tasks],
)
def get_operations(
    user: models.User = Depends(get_current_user),
    operations_service: TasksService = Depends(),
):
    return operations_service.get_many(user.id)


@router.post(
    '/',
    response_model=models.Tasks,
    status_code=status.HTTP_201_CREATED,
)
def create_operation(
    operation_data: models.TasksCreate,
    user: models.User = Depends(get_current_user),
    operations_service: TasksService = Depends(),
):
    return operations_service.create(
        user.id,
        operation_data,
    )


@router.put(
    '/{task_id}',
    response_model=models.Tasks,
)
def update_operation(
    task_id: int,
    operation_data: models.TasksUpdate,
    user: models.User = Depends(get_current_user),
    operations_service: TasksService = Depends(),
):
    return operations_service.update(
        user.id,
        task_id,
        operation_data,
    )


@router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_operation(
    task_id: int,
    user: models.User = Depends(get_current_user),
    operations_service: TasksService = Depends(),
):
    operations_service.delete(
        user.id,
        task_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
