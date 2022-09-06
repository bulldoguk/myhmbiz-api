# user.py

from modules.db.mongodb import get_db_mumshoppe
from typing import Optional, Tuple

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

class Credit(BaseModel):
    optionid: str
    credits: int
    default: str


class Bundle(BaseModel):
    id: Optional[str] = None
    type: str
    size: str
    description: str
    price: float
    credits: list[Credit]


router = APIRouter(
    prefix="/bundles",
    tags=["bundles"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Invalid request"}
    }
)


@router.get("/list")
async def get_bundles():
    return {"name": 'Gary'}


@router.post("/", status_code=200)
async def add_bundle(bundle: Bundle, response: Response):
    if bundle.id:
        response.status_code = status.HTTP_400_E
        return "Invalid request"
    return bundle
