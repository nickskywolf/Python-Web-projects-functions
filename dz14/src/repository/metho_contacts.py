from typing import List, Type

from sqlalchemy.orm import Session

from sqlalchemy import and_
from src.database.db_models import ContactPerson, User
from src.valid_schemas import ContactPersonModel


# ПАПКА REPOSITORY для 5 принципа солида, мы работаем с базой через функции в репозитории, наши
# роуты не меняются в случае если база данных поменяется( с postgres Mongo например

async def rep_create_contact(body: ContactPersonModel, user: User, db: Session) -> ContactPerson:
    """
    The rep_create_contact function creates a new contact in the database.
        Args:
            body (ContactPersonModel): The contact to be created.
            user (User): The user who is creating the contact.
            db (Session): A session for interacting with the database.

    :param body: ContactPersonModel: Get the data from the request body
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A contactperson object
    :doc-author: Trelent
    """
    contact = ContactPerson(
        name=body.name,
        surname=body.surname,
        email=body.email,
        phone=body.phone,
        b_date=body.b_date,
        additional_info=body.additional_info,
        user_id=user.id
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def rep_show_all_contacts(skip: int, user: User, limit: int, db: Session) -> list[Type[ContactPerson]]:
    """
    The rep_show_all_contacts function returns a list of all contacts for the user.
        Args:
            skip (int): The number of items to skip before starting to collect the result set.
            user (User): The User object that is requesting this information.  This is used as a filter in the query, so only contacts associated with this user will be returned.
            limit (int): The maximum number of items to return after skipping &quot;skip&quot; amount of items from the beginning of the result set.

    :param skip: int: Skip the first n records
    :param user: User: Get the user_id from the user object
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the function
    :return: A list of contactperson objects
    :doc-author: Trelent
    """
    return db.query(ContactPerson).filter(ContactPerson.user_id == user.id).offset(skip).limit(limit).all()


async def rep_show_contact(id: int, user: User, db: Session) -> ContactPerson | None:
    """
    The rep_show_contact function is used to retrieve a single contact person from the database.
        The function takes in an id and user object, and returns a ContactPerson object if it exists.

    :param id: int: Specify the id of the contact person
    :param user: User: Make sure that the user is only able to see their own contacts
    :param db: Session: Access the database
    :return: A contact person if it exists
    :doc-author: Trelent
    """
    return db.query(ContactPerson).filter(and_(ContactPerson.id == id, ContactPerson.user_id == user.id)).first()


async def rep_update_contact(id: int, body: ContactPersonModel, user: User, db: Session) -> ContactPerson | None:
    """
    The rep_update_contact function updates a contact in the database.
        Args:
            id (int): The ID of the contact to update.
            body (ContactPersonModel): The updated ContactPerson object to be stored in the database.

    :param id: int: Identify the contact person in the database
    :param body: ContactPersonModel: Get the data from the request body
    :param user: User: Check if the user is logged in and has access to the contact
    :param db: Session: Access the database
    :return: A contactperson object if the contact is found in the database
    :doc-author: Trelent
    """
    contact = db.query(ContactPerson).filter(and_(ContactPerson.id == id, ContactPerson.user_id == user.id)).first()
    if contact:
        ContactPerson.name = body.name
        ContactPerson.surname = body.surname
        ContactPerson.email = body.email
        ContactPerson.phone = body.phone
        ContactPerson.b_date = body.b_date
        ContactPerson.additional_info = body.additional_info

        db.commit()
    return contact


async def rep_remove_contact(id: int, user: User, db: Session) -> ContactPerson | None:
    """
    The rep_remove_contact function removes a contact person from the database.
        Args:
            id (int): The ID of the user to remove.
            user (User): The User object that is being removed from the database.

    :param id: int: Identify the user in the database
    :param user: User: Get the user's id
    :param db: Session: Connect to the database
    :return: A contactperson object if the contact was removed or none if it wasn't
    :doc-author: Trelent
    """
    contact = db.query(ContactPerson).filter(ContactPerson.user_id == user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
