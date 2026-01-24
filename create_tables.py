from api.database import Base, engine
from api.models import Message

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
