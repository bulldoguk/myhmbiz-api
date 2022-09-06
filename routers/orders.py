# orders.py

from optparse import Option
from modules.db.mongodb import get_db_mumshoppe
from pymongo import ReturnDocument
from bson import json_util
import json
import uuid

from typing import Optional

from fastapi import APIRouter, Response, status
from pydantic import BaseModel


# TODO: What else goes into a customer object?


class Customer(BaseModel):
    email: str
    name: str

# Bundle


class Credit(BaseModel):
    sectionguid: str
    credits: int
    default: str


class Bundle(BaseModel):
    guid: str
    shoppe_guid: str
    type: str
    size: str
    description: str
    price: float
    credits: list[Credit]

# Options


class Option(BaseModel):
    optionguid: str
    name: str
    price: float


class Section(BaseModel):
    guid: str
    shoppe_guid: str
    title: str
    notes: Optional[str]
    options: list[Option]


class Order(BaseModel):
    guid: Optional[str] = None
    shoppe_guid: str
    customer: Customer
    bundle: Bundle
    options: list[Section]
    notes: Optional[str]


router = APIRouter(
    prefix="/orders",
    tags=["mumshoppe_orders"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Invalid request"}
    }
)

# TODO: Order statuses (draft, submitted, paid, built, picked up)


@router.get("/list", status_code=status.HTTP_200_OK)
async def get_order(response: Response):
    try:
        order_collection = get_db_mumshoppe().orders.find()
        return json.loads(json_util.dumps(order_collection))
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        print('Failed to list orders', e)
        return None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_order(order: Order, response: Response):
    try:
        order_collection = get_db_mumshoppe().orders
        if not order.guid:
            order.guid = str(uuid.uuid4())
        record = order_collection.find_one_and_update(
            {"guid": order.guid},
            {"$set": order.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        # Remove object id - we're not using that as an index and it breaks Pydantic
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": e}


@router.patch("/{order_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_order(order_id: str, order: Order, response: Response):
    try:
        order_collection = get_db_mumshoppe().orders
        record = order_collection.find_one_and_update(
            {"guid": order_id},
            {"$set": order.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Unable to update order": e}
