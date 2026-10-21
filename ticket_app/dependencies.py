from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ticket_app.auth_service import AuthService, InvalidToken
from ticket_app.service import TicketService
from ticket_app.store import TicketStore
from ticket_app.user_store import UserStore

store = TicketStore()
user_store = UserStore()

bearer = HTTPBearer(auto_error=False)


def get_service() -> TicketService:
    return TicketService(store)


def get_auth_service() -> AuthService:
    return AuthService(user_store)


def get_current_user(
    auth_header: HTTPAuthorizationCredentials | None = Depends(bearer),
    auth: AuthService = Depends(get_auth_service),
) -> dict:
    if auth_header is None:
        raise HTTPException(status_code=401, detail="Not authenticated",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        return auth.user_from_token(auth_header.credentials)
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
