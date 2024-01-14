from pydantic import BaseModel

from .user import User


class ItemBase(BaseModel):
    title: str = None
    dsecription: str = None


class ItemCreate(ItemBase):
    title: str


class ItemUpdate(ItemBase):
    pass


class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class Item(ItemBase):
    pass


class ItemInDB(ItemInDBBase):
    pass

