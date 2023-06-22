# User class mapper
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from config.db import get_connection

# logger
from Imports.logger import getLogger
from models.CategoryModel import Category
from useEnum.Enum import SchemasEnum
log = getLogger(__name__)



def userEntity(item) -> dict:
    return {
        "user_id": item["user_id"],
        "user_type": item["user_type"],
        "first_name": item["first_name"],
        "last_name": item["last_name"],
        "birth_date": item["birth_date"],
        "gender": item["gender"],
        "email": item["email"],
        "mobile": item["mobile"],
        "address": item["address"],
        "addr_no": item["addr_no"],
        "zip_code": item["zip_code"],
        "state": item["state"],
        "city": item["city"],
        "disabled": item["disabled"],
        "last_login": item["last_login"],
        "login_time": item["login_time"]
    }


# User class list mapper
def userListEntity(entity) -> list:
    return [userEntity(item) for item in entity]


# Category class mapper
def categoryEntity(item) -> dict:
    return {
        "cat_id": item["cat_id"],
        "cat_code": item["cat_code"],
        "cat_name": item["cat_name"],
        "cat_desp": item["cat_desp"],
        "disabled": item["disabled"]
    }

# Category class list mapper
def categoryListEntity(entity) -> list:
    return [categoryEntity(item) for item in entity]


# stock class mapper
def stockEntity(item) -> dict:
    db = get_connection()
    try:
        coll = db.get_collection(SchemasEnum.CATEGORY.value)
        category: Category = coll.find_one({"cat_id": item["cat_id"]})

        return {
        "stock_id": item["stock_id"],
        "cat_id": item["cat_id"],
        "stock_code": item["stock_code"],
        "name": item["name"],
        "desp": item["desp"],
        "manufacture": item["manufacture"],
        "filled_no_of_units": item["filled_no_of_units"],
        "sold_no_of_items": item["sold_no_of_items"],
        "available_no_of_items": item["available_no_of_items"],
        "measure_unit": item["measure_unit"],
        "prev_unit_price": item["prev_unit_price"],
        "unit_price": item["unit_price"],
        "curr_code": item["curr_code"],
        "filled_datetime": item["filled_datetime"],
        "created_datetime": item["created_datetime"],
        "updated_datetime": item["updated_datetime"],
        "disabled": item["disabled"],
        "category": category
    }
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")

def stockListEntity(entity) -> list:
    return [stockEntity(item) for item in entity]