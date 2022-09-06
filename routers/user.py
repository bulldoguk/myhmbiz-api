# user.py

from modules.db.mongodb import get_db_common
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel


class User(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


router = APIRouter(
    prefix="/user",
    tags=["common_user"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_user():
    return {"name": 'Gary'}


@router.post("/")
async def add_user(user: User):
    return user
