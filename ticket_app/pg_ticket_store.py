from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from ticket_app.orm_models import Ticket

def _to_dict(ticket: Ticket) -> dict:
    return {
        "id": ticket.id,
        "title": ticket.title,
        "priority": ticket.priority,
        "owner_id": ticket.owner_id,
    }


class PostgresTicketStore:
    def __init__(self, session: Session):
        self.session = session

    def add(self, data: dict) -> dict:
        ticket = Ticket(**data)          # unpacks title=..., priority=..., owner_id=...
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)     # loads the id Postgres generated
        return _to_dict(ticket)

    def title_exists(self, title: str) -> bool:
        the_title_ticket = self.session.scalar(select(Ticket).where(Ticket.title ==title))
        if the_title_ticket is None:
            return False
        return the_title_ticket is not None
        # YOUR PIECE: query the tickets table for this title.
        # Same shape as get_by_username: session.scalar(select(...).where(...))
        # Then turn "Ticket or None" into True/False.
        
    def list_all(self) -> list[dict]:
        all_tickets = self.session.scalars(select(Ticket))
        return [_to_dict(t) for t in all_tickets]
        #can also be ##return [_to_dict(t) for t in self.session.scalrs(select(Ticket))]
    # list_all, id_exists, delete_ticket: next pieces, one at a time

    def id_exists(self, ticket_id:int) -> dict | None:
        ticket = self.session.scalar(select(Ticket).where(Ticket.id == ticket_id))
        return _to_dict(ticket) if ticket is not None else None

    def delete_ticket(self, ticket:dict) -> None:
        self.session.execute(delete(Ticket).where(Ticket.id == ticket["id"]))
        self.session.commit() 