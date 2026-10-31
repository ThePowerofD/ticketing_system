from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ticket_app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), unique=True)
    priority: Mapped[str] = mapped_column(String(20), default="low")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50),unique =True)
    password_hash: Mapped[str] = mapped_column(String(255))


# YOUR PIECE: class User(Base) mapping to a table named "users", with:
#   id            integer primary key
#   username      text up to 50 characters, UNIQUE
#   password_hash text up to 255 characters