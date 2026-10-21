import os
from datetime import datetime, timedelta, timezone

import jwt # type: ignore
from pwdlib import PasswordHash # pyright: ignore[reportMissingImports]

from ticket_app.user_store import UserStore

SECRET = os.environ.get("JWT_SECRET", "dev-only-secret-change-me-in-production")
ALGORITHM = "HS256"
TOKEN_MINUTES = 30


class UsernameTaken(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class InvalidToken(Exception):
    pass


class AuthService:
    def __init__(self, users: UserStore):
        self.users = users
        self.hasher = PasswordHash.recommended()

    def register(self, username: str, password: str) -> dict:
        if self.users.get_by_username(username) is not None:
            raise UsernameTaken(username)
        password_hash = self.hasher.hash(password)
        return self.users.add(username, password_hash)

    def authenticate(self, username: str, password: str) -> dict:
        # find the user by username
        user = self.users.get_by_username(username)
        if user is None or not self.hasher.verify(password, user["password_hash"]):
            raise InvalidCredentials
        # if there's no such user, OR the password doesn't verify against
        return user
        # the stored hash: raise InvalidCredentials()
        # otherwise return the user

    def create_token(self, user: dict) -> str:
        payload = {
            "sub": str(user["id"]),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES),
        }
        return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    def user_from_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        except jwt.InvalidTokenError:
            raise InvalidToken()
        user = self.users.get_by_id(int(payload["sub"]))
        if user is None:
            raise InvalidToken()
        return user