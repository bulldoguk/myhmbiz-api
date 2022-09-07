# options.py

from modules.db.mongodb import get_db_mumshoppe
from pymongo import ReturnDocument
from bson import json_util
import json
import uuid

from typing import Optional

from fastapi import APIRouter, Response, status
from pydantic import BaseModel


class Option(BaseModel):
    optionguid: Optional[str] = None
    name: str
    price: float


class Section(BaseModel):
    guid: Optional[str] = None
    shoppe_guid: str
    title: str
    notes: Optional[str]
    options: list[Option]


router = APIRouter(
    prefix="/options",
    tags=["mumshoppe_options"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Invalid request"}
    }
)

# TODO: CRUD for option items


@router.get("/list/{shoppe_id}", status_code=status.HTTP_200_OK)
async def get_section(shoppe_id: str, response: Response):
    try:
        section_collection = get_db_mumshoppe().options.find({
            "shoppe_guid": shoppe_id
        })
        return json.loads(json_util.dumps(section_collection))
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        print('Failed to list options', e)
        return None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_section(section: Section, response: Response):
    try:
        section_collection = get_db_mumshoppe().options
        if not section.guid:
            section.guid = str(uuid.uuid4())
        record = section_collection.find_one_and_update(
            {"guid": section.guid},
            {"$set": section.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        # Remove object id - we're not using that as an index and it breaks Pydantic
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": e}


@router.patch("/{section_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_section(section_id: str, section: Section, response: Response):
    try:
        section_collection = get_db_mumshoppe().sections
        record = section_collection.find_one_and_update(
            {"guid": section_id},
            {"$set": section.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Unable to update options": e}

#TODO: For each option in a section, if there is no GUID, need to add one before insert / update on that record