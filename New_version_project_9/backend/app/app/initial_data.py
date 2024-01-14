from app.core.logger import logger
from app.db.init_db import init_db
from app.db.session import SessionLocal


def init() -> None:
    db_session = SessionLocal()
    init_db(db_session)


def main() -> None:
    logger.info("Create initial data")
    init()
    logger.info("Initial data created")


if __name__ == '__main__':
    main()
