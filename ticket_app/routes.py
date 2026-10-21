from fastapi import APIRouter, Depends, HTTPException # type: ignore

from ticket_app.dependencies import get_service, get_current_user
from ticket_app.models import TicketIn, TicketOut, UserOut
from ticket_app.service import DuplicateTitle, InvalidPriority, TicketService, TicketNotFound, NoTicketOwner

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketOut, status_code=201)
def create_ticket(ticket: TicketIn, service: TicketService = Depends(get_service), user: dict = Depends(get_current_user)):
    try:
        return service.create(ticket.model_dump(), owner_id=user["id"])
    except InvalidPriority:
        raise HTTPException(status_code=422, detail="priority must be low or high")
    except DuplicateTitle:
        raise HTTPException(status_code=409, detail="duplicate title")


@router.get("", response_model=list[TicketOut])
def list_tickets(service: TicketService = Depends(get_service)):
    return service.list_all()

@router.get("/{ticket_id}", response_model=TicketOut, status_code = 200)
def get_ticket_per_id(ticket_id: int, service: TicketService = Depends(get_service)):
    try: 
        return service.ticket_id_exists(ticket_id)
    except TicketNotFound:
        raise HTTPException(status_code=404, detail="TicketNotFound")

@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_service),
    user: dict = Depends(get_current_user),
):
    try:
        service.delete(ticket_id, user_id=user["id"])
    except TicketNotFound:
        raise HTTPException(status_code=404, detail="Ticket not found")
    except NoTicketOwner:
        raise HTTPException(status_code=403, detail="Not your ticket")