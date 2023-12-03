from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URL = "postgresql+psycopg2://postgres:567234@localhost:5432/postgres"


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db_func():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
