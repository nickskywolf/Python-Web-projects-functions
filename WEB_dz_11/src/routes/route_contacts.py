from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db_connection import get_db_func
from src.valid_schemas import ContactPersonModel
from src.repository import metho_contacts

router = APIRouter(prefix='/contacts')


@router.post("/")
async def create_contact(body: ContactPersonModel, db: Session = Depends(get_db_func)):
    return await metho_contacts.rep_create_contact(body, db)


@router.get("/")
async def read_contacts(db: Session = Depends(get_db_func)):
    contacts = await metho_contacts.rep_show_all_contacts(db)
    return contacts


@router.get("/{id}")
async def read_contact(id: int, db: Session = Depends(get_db_func)):
    contact = await metho_contacts.rep_show_contact(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{id}")
async def update_contact(body: ContactPersonModel, id: int, db: Session = Depends(get_db_func)):
    contact = await metho_contacts.rep_update_contact(id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{id}")
async def remove_contact(id: int, db: Session = Depends(get_db_func)):
    contact = await metho_contacts.rep_remove_contact(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
