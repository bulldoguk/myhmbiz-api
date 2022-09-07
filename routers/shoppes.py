# shoppes.py

from dataclasses import replace
from modules.db.mongodb import get_db_mumshoppe
from pymongo import ReturnDocument
from bson import json_util
import json
import uuid

from typing import Optional

from fastapi import APIRouter, Response, status
from pydantic import BaseModel


class Shoppe(BaseModel):
    guid: Optional[str] = None
    title: str
    school: str
    contact_email: Optional[str]
    contact_name: Optional[str]
    contact_phone: Optional[str]
    notes: Optional[str]
    slug: Optional[str]


router = APIRouter(
    prefix="/shoppes",
    tags=["mumshoppe_shoppes"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Invalid request"}
    }
)


@router.get("/list", status_code=status.HTTP_200_OK)
async def get_shoppes(response: Response):
    try:
        shoppes_collection = get_db_mumshoppe().shoppes.find()
        return json.loads(json_util.dumps(shoppes_collection))
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        print('Failed to list options', e)
        return None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_shoppe(shoppe: Shoppe, response: Response):
    try:
        shoppes_collection = get_db_mumshoppe().shoppes
        if not shoppe.guid:
            shoppe.guid = str(uuid.uuid4())
        if not shoppe.slug:
            shoppe.slug = str.replace(shoppe.title, ' ', '_')
        record = shoppes_collection.find_one_and_update(
            {"guid": shoppe.guid},
            {"$set": shoppe.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        # Remove object id - we're not using that as an index and it breaks Pydantic
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": e}


@router.patch("/{shoppe_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_shoppe(shoppe_id: str, shoppe: Shoppe, response: Response):
    try:
        shoppes_collection = get_db_mumshoppe().shoppes
        if not shoppe.slug:
            shoppe.slug = str.replace(shoppe.title, ' ', '_')
        record = shoppes_collection.find_one_and_update(
            {"guid": shoppe_id},
            {"$set": shoppe.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Unable to update Shoppes": e}
