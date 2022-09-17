from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    mode = Column(String)
    username = Column(String, unique=True)
    password_hash = Column(String)


class UserDataHH(Base):
    __tablename__ = 'users_hh'

    id = Column(Integer, primary_key=True)
    telegarm_id = Column(Integer, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    phone = Column(String, unique=True)
    password = Column(String)
    proxy = Column(String)
    hhtoken = Column(String)
    xsrf = Column(String)

    user = relationship('User', backref='users_hh')


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)

    owner = Column(Integer, ForeignKey('users_hh.telegarm_id'), index=True)
    title = Column(String)
    resume_id = Column(String, unique=True)

    last_launch = Column(String)

    user_hh = relationship('UserDataHH', backref='tasks')
