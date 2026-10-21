from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore

app = FastAPI()


class TicketIn(BaseModel):
    title: str
    priority: str = "low"
    internal_note: str


class TicketOut(BaseModel):
    id: int
    title: str
    priority: str


tickets = []


@app.post("/tickets", response_model=TicketOut, status_code=201)
def create_ticket(ticket: TicketIn):
    record = {"id": len(tickets) + 1, **ticket.model_dump()}
    tickets.append(record)
    return record

@app.get("/tickets/{ticket_id}", response_model=TicketOut, status_code=200)
def get_tickets(ticket_id: int):
    for record in tickets:
        if record["id"] == ticket_id:
            return record
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/tickets", response_model=list[TicketOut], status_code=200)
def get_all_tickets(priority: str | None = None):
    req_list = []
    if priority == None:
        return tickets
    else:
        for tic in tickets:
            if tic["priority"] == priority:
                req_list.append(tic)
        return req_list

### return [tic for tic in tickets if tic["priority"] == priority]
