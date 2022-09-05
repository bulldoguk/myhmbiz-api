# user.py

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel


class User(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


router = APIRouter()


@router.get("/user")
async def get_user():
    return {"name": 'Gary'}


@router.post("/user")
async def add_user(user: User):
    return user
