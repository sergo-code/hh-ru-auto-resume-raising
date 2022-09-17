from pydantic import BaseModel


class BaseUserDataHH(BaseModel):
    telegarm_id: int
    phone: str
    password: str
    proxy: str
    hhtoken: str
    xsrf: str


class UserDataHHCreate(BaseUserDataHH):
    pass


class UserDataHHUpdate(BaseUserDataHH):
    pass


class UserDataHH(BaseUserDataHH):
    id: int

    class Config:
        orm_mode = True
