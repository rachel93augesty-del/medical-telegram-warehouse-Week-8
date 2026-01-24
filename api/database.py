# api/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = "postgres"
DB_PASSWORD = "Rachelsemer@db93"  # your password
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "medical_warehouse"

# Use URL encoding for special characters like @
from urllib.parse import quote_plus
DB_PASSWORD_ENC = quote_plus(DB_PASSWORD)

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD_ENC}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
