from typing import List, Type

from sqlalchemy.orm import Session

from src.database.db_models import ContactPerson
from src.valid_schemas import ContactPersonModel


# ПАПКА REPOSITORY для 5 принципа солида, мы работаем с базой через функции в репозитории, наши
# роуты не меняются в случае если база данных поменяется( с postgres Mongo например

async def rep_create_contact(body: ContactPersonModel, db: Session) -> ContactPerson:
    contact = ContactPerson(
        name=body.name,
        surname=body.surname,
        email=body.email,
        phone=body.phone,
        b_date=body.b_date,
        additional_info=body.additional_info,
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def rep_show_all_contacts(skip: int, limit: int, db: Session) -> list[Type[ContactPerson]]:
    return db.query(ContactPerson).offset(skip).limit(limit).all()


async def rep_show_contact(id: int, db: Session) -> ContactPerson | None:
    return db.query(ContactPerson).filter(ContactPerson.id == id).first()


async def rep_update_contact(id: int, body: ContactPersonModel, db: Session) -> ContactPerson | None:
    contact = db.query(ContactPerson).filter(ContactPerson.id == id).first()
    if contact:
        ContactPerson.name = body.name
        ContactPerson.surname = body.surname
        ContactPerson.email = body.email
        ContactPerson.phone = body.phone
        ContactPerson.b_date = body.b_date
        ContactPerson.additional_info = body.additional_info

        db.commit()
    return contact


async def rep_remove_contact(id: int, db: Session) -> ContactPerson | None:
    contact = db.query(ContactPerson).filter(ContactPerson.id == id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
