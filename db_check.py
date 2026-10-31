import os

from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:secret@localhost:5432/tickets",
)

engine = create_engine(DATABASE_URL, echo=True)     # echo=True prints every SQL statement

with engine.connect() as conn:
    print("server version:", conn.execute(text("SELECT version()")).scalar())
    print("current database:", conn.execute(text("SELECT current_database()")).scalar())
    print("2 + 3 =", conn.execute(text("SELECT :a + :b"), {"a": 2, "b": 3}).scalar())