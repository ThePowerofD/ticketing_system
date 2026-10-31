from sqlalchemy import select
from sqlalchemy.orm import Session

from ticket_app.orm_models import User


def _to_dict(user: User) -> dict:
    return {"id": user.id, "username": user.username, "password_hash": user.password_hash}


class PostgresUserStore:
    def __init__(self, session: Session):
        self.session = session

    def add(self, username: str, password_hash: str) -> dict:
        user = User(username=username, password_hash=password_hash)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return _to_dict(user)

    def get_by_username(self, username: str) -> dict | None:
        user = self.session.scalar(select(User).where(User.username == username))
        return _to_dict(user) if user else None
        

    def get_by_id(self, user_id: int) -> dict | None:
        user = self.session.get(User, user_id)
        return _to_dict(user) if user else None 