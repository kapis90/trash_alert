from typing import Optional
from pydantic import BaseModel
from datetime import date


class User(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[int] = None
    street_id: Optional[int] = None


class Area(BaseModel):
    id: int
    name: str


class Street(BaseModel):
    id: int
    name: str
    area_id: int


class PickUpDate(BaseModel):
    date: date
    area_id: int
    type: str
