from fastapi import APIRouter, Depends, HTTPException # pyright: ignore[reportMissingImports]

from ticket_app.auth_service import AuthService, InvalidCredentials, UsernameTaken
from ticket_app.dependencies import get_auth_service, get_current_user
from ticket_app.models import TokenOut, UserIn, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


# YOUR PIECE: POST /auth/register
# - body: UserIn
# - gets the service with Depends(get_auth_service)
# - returns the new user, filtered by response_model=UserOut, status 201
# - UsernameTaken → 409 with detail "Username already taken"

@router.post("/register", response_model=UserOut, status_code=201)
def user_register(credentials: UserIn, auth: AuthService = Depends(get_auth_service)):
    try:
        new_user = auth.register(credentials.username, credentials.password)
        return new_user
    except UsernameTaken:
        raise HTTPException(status_code=409, detail="Username already Taken")


@router.post("/login", response_model=TokenOut)
def login(credentials: UserIn, auth: AuthService = Depends(get_auth_service)):
    try:
        user = auth.authenticate(credentials.username, credentials.password)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": auth.create_token(user), "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def me(user: dict = Depends(get_current_user)):
    return user