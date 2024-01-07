from typing import List, Optional
import re

from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from pydantic.schema import date, datetime


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactPersonModel(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr
    phone: str
    b_date: Optional[date]
    additional_info: str = Field(max_length=500)

    @validator('phone')
    def real_phone(cls, phone, **kwargs):
        """
        The real_phone function validates that the phone number is in a real format.
            Args:
                phone (str): The phone number to validate.

        :param cls: Pass the class that is being validated
        :param phone: Store the phone number
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A string that is a phone number,
        :doc-author: Trelent
        """
        regex = r"^(\+)[0-9]{9,18}$"
        result = re.findall(regex, phone)
        if not result:
            raise HTTPException(status_code=400, detail='Phone: стандарт префикс "+" и 15 цифр, Германия  18')
        return phone

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class RequestEmail(BaseModel):
    email: EmailStr
