from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db_connection import get_db_func
from src.database.db_models import User
from src.valid_schemas import ContactPersonModel
from src.repository import metho_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts')


@router.post("/")
async def create_contact(body: ContactPersonModel, db: Session = Depends(get_db_func),
                         current_user: User = Depends(auth_service.get_current_user)):
    return await metho_contacts.rep_create_contact(body, current_user, db)


@router.get("/")
async def read_contacts(db: Session = Depends(get_db_func),
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await metho_contacts.rep_show_all_contacts(db)
    return contacts


@router.get("/{id}")
async def read_contact(id: int, db: Session = Depends(get_db_func),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await metho_contacts.rep_show_contact(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{id}")
async def update_contact(body: ContactPersonModel, id: int, db: Session = Depends(get_db_func),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await metho_contacts.rep_update_contact(id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{id}")
async def remove_contact(id: int, db: Session = Depends(get_db_func),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await metho_contacts.rep_remove_contact(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
