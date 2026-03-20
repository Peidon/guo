
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

try:
    engine = create_engine(settings.DB_URL)
    SessionLocal = sessionmaker(bind=engine)
except Exception as e:
    print(f"An error occurred: {e}")