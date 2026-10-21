from datetime import datetime, timedelta, timezone

import jwt

SECRET = "change-me-to-a-long-random-string"     # a real app reads this from an environment variable
ALGORITHM = "HS256"

# --- login succeeded: create a token ---
payload = {
    "sub": "5",                                                  # "subject": who the token is about (user id, as text)
    "exp": datetime.now(timezone.utc) + timedelta(minutes=30),    # expires in 30 minutes
}
token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
print("token:", token)

# --- every request: check the token ---
data = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
print("decoded:", data)

# --- someone edits the payload (user 1, expiring far in the future) ---
header, body, signature = token.split(".")
fake_body = jwt.utils.base64url_encode(b'{"sub":"1","exp":9999999999}').decode()
edited = f"{header}.{fake_body}.{signature}"
try:
    jwt.decode(edited, SECRET, algorithms=[ALGORITHM])
except jwt.InvalidSignatureError:
    print("edited token: rejected (InvalidSignatureError)")

# --- a token that expired a minute ago ---
old = jwt.encode(
    {"sub": "5", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
    SECRET,
    algorithm=ALGORITHM,
)
try:
    jwt.decode(old, SECRET, algorithms=[ALGORITHM])
except jwt.ExpiredSignatureError:
    print("expired token: rejected (ExpiredSignatureError)")

# --- checked with the wrong secret ---
try:
    jwt.decode(token, "a-completely-different-secret-key", algorithms=[ALGORITHM])
except jwt.InvalidSignatureError:
    print("wrong secret: rejected (InvalidSignatureError)")