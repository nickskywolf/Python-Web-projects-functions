from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db_connection import get_db_func
from src.database.db_models import User
from src.valid_schemas import ContactPersonModel
from src.repository import metho_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts')


@router.post("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(body: ContactPersonModel, db: Session = Depends(get_db_func),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactPersonModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user id of the logged in user
    :return: A contactpersonmodel object
    :doc-author: Trelent
    """
    return await metho_contacts.rep_create_contact(body, current_user, db)


@router.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def read_contacts(db: Session = Depends(get_db_func),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of all contacts in the database.
        The function is called by sending a GET request to the /contacts endpoint.

    :param db: Session: Access the database
    :param current_user: User: Get the user who is making the request
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await metho_contacts.rep_show_all_contacts(db)
    return contacts


@router.get("/{id}", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def read_contact(id: int, db: Session = Depends(get_db_func),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact function is used to read a single contact from the database.
    It takes an id as input and returns a Contact object if found, otherwise it raises an HTTPException.

    :param id: int: Get the id of the contact to be updated
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await metho_contacts.rep_show_contact(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{id}", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def update_contact(body: ContactPersonModel, id: int, db: Session = Depends(get_db_func),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, which is then used to update the contact.
        If no contact with that id exists, it returns 404 Not Found.

    :param body: ContactPersonModel: Get the data that will be updated
    :param id: int: Identify the contact to be deleted
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A contactpersonmodel object
    :doc-author: Trelent
    """
    contact = await metho_contacts.rep_update_contact(id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{id}", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def remove_contact(id: int, db: Session = Depends(get_db_func),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param id: int: Specify the id of the contact to be removed
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is logged in
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await metho_contacts.rep_remove_contact(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
