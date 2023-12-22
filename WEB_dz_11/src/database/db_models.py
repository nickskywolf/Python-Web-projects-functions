from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
#Base.metadata.create_all(bind=engine)


class ContactPerson(Base):
    __tablename__ = "Contacts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(256)) # 256 - max
    phone = Column(String(19)) # стандарт префикс "+" и 15 цифр но в германии есть 18
    b_date = Column(Date, nullable=True, default='...No birthday date, yet...')
    additional_info = Column(String(500), nullable=True, default='...No additional information provided...')