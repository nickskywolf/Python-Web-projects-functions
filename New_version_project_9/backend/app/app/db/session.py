
from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from app.core.config import settings




engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
# db_session = scoped_session(
#     sessionmaker(autocommit=False, autoflush=False, bind=engine)
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
