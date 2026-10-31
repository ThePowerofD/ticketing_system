from ticket_app.database import Base, engine
from ticket_app import orm_models  # noqa: F401  (importing registers the models on Base)

Base.metadata.create_all(engine)
print("tables created")