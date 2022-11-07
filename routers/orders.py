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
    orderTitle: str
    KHSBandMember: Optional[bool] = False
    KHSBandMemberColorGuard: Optional[bool] = False
    OKToText: Optional[bool] = False
    bandInstrument: Optional[str] = ''
    cellPhone: str
    orderDate: str

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


class RibbonNames(BaseModel):
    ribbonName1: Optional[str] = None
    grade1: Optional[str] = None
    activity1: Optional[str] = None
    school1: Optional[str] = None
    ribbonName2: Optional[str] = None
    grade2: Optional[str] = None
    activity2: Optional[str] = None
    school2: Optional[str] = None

# Options


class Option(BaseModel):
    optionguid: str
    name: str
    price: float


class Section(BaseModel):
    section: str
    optionguid: str
    name: str
    price: float
    position: int


class Order(BaseModel):
    guid: Optional[str] = None
    status: Optional[str] = 'draft'
    shoppe_guid: str
    customer: Customer
    ribbonNames: Optional[RibbonNames] = None
    bundle: Optional[Bundle] = None
    options: list[Section]
    notes: Optional[str]
    shoppeInfo: Optional[list] = None


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


@router.get("/listByCustomer", status_code=status.HTTP_200_OK)
async def get_orders_by_customer(email: str, response: Response):
    try:
        order_collection = get_db_mumshoppe().orders.aggregate([
            {
                '$lookup': {
                    'from': 'shoppes', 
                    'localField': 'shoppe_guid', 
                    'foreignField': 'guid', 
                    'as': 'shoppeInfo'
                }
            }, {
                '$limit': 1
            }
        ])
        # order_collection = get_db_mumshoppe().orders.find(
         #   {"customer.email": email}
        # 
        result = json.loads(json_util.dumps(order_collection))
        return result
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None


@router.get("/byId", status_code=status.HTTP_200_OK)
async def get_order_by_id(orderid: str, response: Response):
    try:
        record = get_db_mumshoppe().orders.find_one(
            {"guid": orderid}
        )
        # Remove object id - we're not using that as an index and it breaks Pydantic
        del record["_id"]
        print(f'Record {record}')
        return record
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Error": e}


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


# @router.patch("/{order_id}", status_code=status.HTTP_202_ACCEPTED)
@router.patch("/", status_code=status.HTTP_202_ACCEPTED)
async def update_order(order: Order, response: Response):
    try:
        order_collection = get_db_mumshoppe().orders
        # Need to use this method to create a new order if none exists
        if not order.guid:
            order.guid = str(uuid.uuid4())
        record = order_collection.find_one_and_update(
            {"guid": order.guid},
            {"$set": order.dict()},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        del record["_id"]
        return record
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Unable to update order": e}
