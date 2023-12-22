from typing import List, Optional
import re

from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from pydantic.schema import date


class ContactPersonModel(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: str = EmailStr
    phone: str
    b_date: Optional[date]
    additional_info: str = Field(max_length=500)

    @validator('phone')
    def real_phone(cls, phone, **kwargs):
        regex = r"^(\+)[0-9]{9,18}$"
        result = re.findall(regex, phone)
        if not result:
            raise HTTPException(status_code=400, detail='Phone: стандарт префикс "+" и 15 цифр, Германия  18')
        return phone

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
