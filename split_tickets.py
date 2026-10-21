from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# ---------- models: shapes of the data ----------
class TicketIn(BaseModel):
    title: str
    priority: str = "low"


class TicketOut(BaseModel):
    id: int
    title: str
    priority: str


# ---------- 1. STORAGE: keeps data and finds it again ----------
class TicketStore:
    def __init__(self):
        self._tickets = []
        self._next_id = 1

    def add(self, data: dict) -> dict:
        record = {"id": self._next_id, **data}
        self._next_id += 1
        self._tickets.append(record)
        return record

    def title_exists(self, title: str) -> bool:
        return any(t["title"] == title for t in self._tickets)


# ---------- 2. SERVICE: business rules, no HTTP ----------
class InvalidPriority(Exception):
    pass


class DuplicateTitle(Exception):
    pass


class TicketService:
    def __init__(self, store: TicketStore):
        self.store = store

    def create(self, data: dict) -> dict:
        if data["priority"] not in ("low", "high"):
            raise InvalidPriority(data["priority"])
        if self.store.title_exists(data["title"]):
            raise DuplicateTitle(data["title"])
        return self.store.add(data)


# ---------- 3. ROUTE: HTTP only ----------
store = TicketStore()
service = TicketService(store)


@app.post("/tickets", response_model=TicketOut, status_code=201)
def create_ticket(ticket: TicketIn):
    try:
        return service.create(ticket.model_dump())
    except InvalidPriority:
        raise HTTPException(status_code=422, detail="priority must be low or high")
    except DuplicateTitle:
        raise HTTPException(status_code=409, detail="duplicate title")