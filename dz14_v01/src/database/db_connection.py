from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings

DB_URL = settings.sqlalchemy_database_url


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db_func():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
