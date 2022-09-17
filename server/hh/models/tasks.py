from pydantic import BaseModel


class BaseTasks(BaseModel):
    title: str
    resume_id: str
    last_launch: str


class TasksCreate(BaseTasks):
    pass


class TasksUpdate(BaseTasks):
    pass


class Tasks(BaseTasks):
    id: int

    class Config:
        orm_mode = True
