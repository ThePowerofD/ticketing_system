from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from ticket_app import auth_routes, routes
from ticket_app.dependencies import get_session

app = FastAPI()
app.include_router(routes.router)
app.include_router(auth_routes.router)

@app.get("/health/db")
def db_health(session: Session = Depends(get_session)):
    session.execute(text("SELECT 1"))
    return {"database": "ok"}
