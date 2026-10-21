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

    def list_all(self) -> list[dict]:
        return list(self._tickets)

    def id_exists(self, ticket_id:int):
        for ticket in self._tickets:
            if ticket["id"] == ticket_id:
                return ticket
        return None

    def delete_ticket(self, ticket:dict) -> None:
        self._tickets.remove(ticket)