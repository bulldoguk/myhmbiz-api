# user.py

from modules.db.mongodb import get_db_mumshoppe
from pymongo import ReturnDocument

import uuid

from typing import Optional

from fastapi import APIRouter, Response, status
from pydantic import BaseModel


class Credit(BaseModel):
    optionid: str
    credits: int
    default: str


class Bundle(BaseModel):
    guid: Optional[str] = None
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
        400: {"description": "Invalid request"}
    }
)


@router.get("/list", status_code=status.HTTP_200_OK)
async def get_bundles():
    return {"name": 'Gary'}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_bundle(bundle: Bundle, response: Response):
    try:
        event_collection = get_db_mumshoppe().bundles
        if not bundle.guid:
            bundle.guid = str(uuid.uuid4())
        record = event_collection.find_one_and_update(
            {"guid": bundle.guid},
            {"$set": bundle.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": e}


@router.patch("/", status_code=status.HTTP_202_ACCEPTED)
async def update_bundle(bundle: Bundle, response: Response):
    if not bundle.id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Bundle ID is missing"
    return bundle
