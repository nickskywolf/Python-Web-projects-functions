from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

DATABASE_URL = "postgresql://nickuser:nick1993pass@localhost/nick_db"

# Створення базової моделі SQLAlchemy
Base = declarative_base()


# Оголошення моделі для контактів
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    birthday = Column(Date)
    additional_data = Column(String, nullable=True)


# Створення бази даних
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Створення сесії бази даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI об'єкт
app = FastAPI()


# Pydantic модель для валідації даних контакту
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: str = None


# Маршрути API


# Створення нового контакту
@app.post("/contacts/", response_model=ContactCreate)
def create_contact(contact: ContactCreate):
    db = SessionLocal()
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    db.close()
    return db_contact


# Отримання списку всіх контактів
@app.get("/contacts/")
def read_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    name_query: str = None,
    email_query: str = None,
):
    db = SessionLocal()
    contacts = db.query(Contact).offset(skip).limit(limit)
    if name_query:
        contacts = contacts.filter(
            (Contact.first_name.contains(name_query))
            | (Contact.last_name.contains(name_query))
        )
    if email_query:
        contacts = contacts.filter(Contact.email.contains(email_query))
    db.close()
    return contacts.all()


# Отримання одного контакту за ідентифікатором
@app.get("/contacts/{contact_id}")
def read_contact(contact_id: int):
    db = SessionLocal()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()
    if contact:
        return contact
    raise HTTPException(status_code=404, detail="Contact not found")


# Оновлення існуючого контакту
@app.put("/contacts/{contact_id}", response_model=ContactCreate)
def update_contact(contact_id: int, updated_contact: ContactCreate):
    db = SessionLocal()
    existing_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if existing_contact:
        for field, value in updated_contact.dict().items():
            setattr(existing_contact, field, value)
        db.commit()
        db.refresh(existing_contact)
        db.close()
        return existing_contact
    db.close()
    raise HTTPException(status_code=404, detail="Contact not found")


# Видалення контакту
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    db = SessionLocal()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
        db.close()
        return {"message": "Contact deleted"}
    db.close()
    raise HTTPException(status_code=404, detail="Contact not found")


# Отримання списку контактів з днями народження на найближчі 7 днів
@app.get("/contacts/birthdays/")
def upcoming_birthdays():
    db = SessionLocal()
    today = date.today()
    seven_days_later = today + timedelta(days=7)
    upcoming_birthdays_list = db.query(Contact).filter(
        (Contact.birthday >= today) & (Contact.birthday <= seven_days_later)
    )
    db.close()
    return upcoming_birthdays_list.all()
