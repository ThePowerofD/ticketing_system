from fastapi import FastAPI

from ticket_app import auth_routes, routes

app = FastAPI()
app.include_router(routes.router)
app.include_router(auth_routes.router)