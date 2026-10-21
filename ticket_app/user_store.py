class UserStore:
    def __init__(self):
        self._users = []
        self._next_id = 1

    def add(self, username: str, password_hash: str) -> dict:
        # build the record (id, username, password_hash), increase the counter,
        # save it in the list, and return it
        record = {"id": self._next_id, "username": username, "password_hash":password_hash}
        self._next_id += 1
        self._users.append(record)
        return record

    def get_by_username(self, username: str) -> dict | None:
        # return the user with that username, or None
        for user in self._users:
            if user["username"] == username:
                return user
        return None

    def get_by_id(self, user_id: int) -> dict | None:
        # return the user with that id, or None
        for user in self._users:
            if user["id"] == user_id:
                return user
        return None