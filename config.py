from server.hh.database import engine
from server.hh.tables import Base
from server.hh.tables import User
from server.hh.settings import settings

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from passlib.hash import bcrypt


class Setup:
    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def create_db(cls):
        Base.metadata.create_all(engine)

    def create_user(self, username: str, mode: str, password_hash: str) -> str:
        user = User(
            username=username,
            mode=mode,
            password_hash=self.hash_password(password_hash)
        )

        engine = create_engine(settings.database_url)
        session = Session(bind=engine)
        session.add(user)
        session.commit()

        return 'User created!'


obj = Setup()
obj.create_db()
user = obj.create_user(username='sergo-code', mode='Admin', password_hash='123456')
print(user)
