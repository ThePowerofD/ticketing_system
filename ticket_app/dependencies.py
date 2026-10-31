from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ticket_app.auth_service import AuthService, InvalidToken
from ticket_app.service import TicketService
from ticket_app.store import TicketStore
from ticket_app.user_store import UserStore
from ticket_app.database import SessionLocal
from sqlalchemy.orm import Session                          # ← NEW
from ticket_app.pg_user_store import PostgresUserStore  
    # ← NEW
from ticket_app.pg_ticket_store import PostgresTicketStore

bearer = HTTPBearer(auto_error=False)




def get_session():
    session = SessionLocal()
    print("session opened")
    try:
        yield session
    finally:
        session.close()
        print("session closed")

def get_service(session: Session = Depends(get_session)) -> TicketService:
    return TicketService(PostgresTicketStore(session))

def get_auth_service(session: Session = Depends(get_session)) -> AuthService:   # ← NEW: needs a session
    return AuthService(PostgresUserStore(session))                               # ← NEW: the Postgres store


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