from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

from typing import List

from .books import IncomingBook, BaseBook,ReturnedBook


__all__ = ["NewSeller","ReturnedSeller","BaseSeller", "ReturnedAllSells"]


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


class NewSeller(BaseSeller):
    books: list[ReturnedBook]
    password: str

class ReturnedSeller(BaseSeller):
    id: int
    books: list[ReturnedBook]

class ReturnedAllSells(BaseModel):
    sellers: list[ReturnedSeller]