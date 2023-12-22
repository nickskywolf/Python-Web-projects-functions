
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta  # Додано бібліотеку для роботи з датами
from .database import SessionLocal, engine
from .models import Base, Contact
from .authentication import get_current_user

Base.metadata.create_all(bind=engine)

app = APIRouter()


@app.post("/contacts/", response_model=Contact)
async def create_contact(
    contact: Contact,
    db: Session = Depends(SessionLocal),
    current_user: User = Depends(get_current_user),
):
    db_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get("/contacts/", response_model=list[Contact])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(SessionLocal),
    current_user: User = Depends(get_current_user),
):
    contacts = (
        db.query(Contact)
        .filter(Contact.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contacts


# Add other CRUD operations for contacts as needed
