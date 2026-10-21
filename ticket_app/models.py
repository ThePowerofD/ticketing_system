from pydantic import BaseModel # pyright: ignore[reportMissingImports]


class TicketIn(BaseModel):
    title: str
    priority: str = "low"


class TicketOut(BaseModel):
    id: int
    title: str
    priority: str
    owner_id: int

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str



