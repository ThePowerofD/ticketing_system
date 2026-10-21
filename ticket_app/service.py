from ticket_app.store import TicketStore


class InvalidPriority(Exception):
    pass


class DuplicateTitle(Exception):
    pass

class TicketNotFound(Exception):
    pass

class NoTicketOwner(Exception):
    ...


class TicketService:
    def __init__(self, store: TicketStore):
        self.store = store

    def create(self, data: dict, owner_id: int) -> dict:
        if data["priority"] not in ("low", "high"):
            raise InvalidPriority(data["priority"])
        if self.store.title_exists(data["title"]):
            raise DuplicateTitle(data["title"])
        return self.store.add({**data, "owner_id":owner_id})

    def list_all(self) -> list[dict]:
        return self.store.list_all()
    
    def ticket_id_exists(self, ticket_id: int)-> dict:
        ticket = self.store.id_exists(ticket_id)
        if ticket is None:
            raise TicketNotFound(ticket_id)
        return ticket

    def delete(self, ticket_id: int, user_id: int) -> None:
        ticket = self.ticket_id_exists(ticket_id)
        #Not necessary already existant in ticket_id_exists
        #if ticket is None:
        #    raise TicketNotFound(ticket_id)
        if ticket["owner_id"]!=user_id:
            raise NoTicketOwner(ticket_id)
        self.store.delete_ticket(ticket)