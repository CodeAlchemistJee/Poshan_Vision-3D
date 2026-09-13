from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Grab the Neon connection URL from Render's environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the database with pool_pre_ping to prevent sleep disconnects
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()