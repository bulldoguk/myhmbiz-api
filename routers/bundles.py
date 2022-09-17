# bundles.py

from operator import truediv
from modules.db.mongodb import get_db_mumshoppe
from modules.auth import token
from pymongo import ReturnDocument
from bson import json_util
import json

import uuid

from typing import Optional

from fastapi import APIRouter, Response, status, Depends
from pydantic import BaseModel


class Credit(BaseModel):
    sectionguid: str
    credits: int
    default: str


class Bundle(BaseModel):
    guid: Optional[str] = None
    shoppe_guid: str
    position: Optional[int] = 0
    type: str
    size: str
    description: str
    price: float
    credits: list[Credit]


router = APIRouter(
    prefix="/bundles",
    tags=["mumshoppe_bundles"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Invalid request"}
    }
)


@router.get("/list/{shoppe_id}", status_code=status.HTTP_200_OK)
async def get_bundles(shoppe_id: str, response: Response):
    try:
        bundle_collection = get_db_mumshoppe().bundles.find({
            "shoppe_guid": shoppe_id
        })
        return json.loads(json_util.dumps(bundle_collection))
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        print('Failed to list bundles', e)
        return None


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
        # Remove object id - we're not using that as an index and it breaks Pydantic
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": e}


@router.patch("/{bundle_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_bundle(bundle_id: str, bundle: Bundle, response: Response):
    try:
        event_collection = get_db_mumshoppe().bundles
        record = event_collection.find_one_and_update(
            {"guid": bundle_id},
            {"$set": bundle.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Unable to update bundle": e}


@router.delete('/{bundle_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_bundle(bundle_id: str, response: Response):
    try:
        bundle_collection = get_db_mumshoppe().bundles
        record = bundle_collection.find_one_and_delete(
            {"guid": bundle_id},
        )
        return True
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Unable to delete bundle": e}
