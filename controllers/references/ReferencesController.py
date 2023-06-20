from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from os import environ as env
from Security.AuthService import get_current_active_user, oauth_2_schema
from config.db import get_connection
from models.CategoryModel import Category
from models.error.ErrorModel import BadAlertException
from models.response.CreateResponseModel import CreateResponseModel
from models.response.DeleteResponseModel import DeleteResponse
from useEnum.Enum import SchemaSequencesEnum, SchemasEnum
from utils.common.SequenceGenerator import get_next_sequence_value
from models.response.ResponseTemplateModes import categoryEntity, categoryListEntity

# logger
from Imports.logger import getLogger
log = getLogger(__name__)

router = APIRouter(
    prefix=f"{env['BASE_URL']}"+'/reference',
    tags=['references'],
    dependencies=[Depends(oauth_2_schema), Depends(get_current_active_user)]
)


## category controller
## category apis
@router.post("/category", status_code=status.HTTP_201_CREATED)
async def add_new_category(category: Category):
    log.info("create new category called")
    # get db connection
    db = get_connection()
    try:

        # dto validate
        if (category.cat_code == '' or category.cat_code == 'null'):
            raise BadAlertException('Category code is required')
        if (category.cat_name == '' or category.cat_name == 'null'):
            raise BadAlertException('Category name is required')

        # set disabled false
        category.disabled = False

        # validate category code already exists
        cat_exists = db.get_collection(
            SchemasEnum.CATEGORY.value).find_one({"cat_code": category.cat_code})
        if cat_exists:
            raise BadAlertException("Category already exists by inserted category code.")

        # generate sequence and insert to dto
        category.cat_id = get_next_sequence_value(
            SchemasEnum.SEQUENCES.value, SchemaSequencesEnum.CATEGORY.value, db)
        
        # save
        result = db[SchemasEnum.CATEGORY.value].insert_one(dict(category))
        return CreateResponseModel(id=str(category.cat_id), status="success", desc="Category creation successful")
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        

@router.get("/categories", response_model=list[Category], status_code=status.HTTP_200_OK)
async def get_all_categories():
    log.info("get all categories called")
    try:
        db = get_connection().get_collection(SchemasEnum.CATEGORY.value)
        cat_list: list[Category] = categoryListEntity(db.find({"disabled":False}))
        return cat_list
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        

@router.get("/category/cat_id/{cat_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get_category_by_cat_id(cat_id: int):
    log.info("get category by cat id called")
    
    try:
        db = get_connection().get_collection(SchemasEnum.CATEGORY.value)
        
        cat_exists = db.find_one({"cat_id":cat_id, "disabled": False})

        # validate
        if cat_exists is None:
            raise BadAlertException("Category not exists.")
        
        return categoryEntity(cat_exists)
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        
    
@router.put("/category/cat_id/{cat_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def update_category_by_cat_id(cat_id: int, category: Category):
    log.info("update category by cat id called")
    try:
        db = get_connection().get_collection(SchemasEnum.CATEGORY.value)
    
        cat_exists = db.find_one({"cat_id":cat_id, "disabled": False})

        # validate
        if cat_exists is None:
            raise BadAlertException("Category not exists.")
        # dto validate
        if (category.cat_name == '' or category.cat_name == 'null'):
            raise BadAlertException('Category name is required')
        if (category.cat_id != cat_id):
            raise BadAlertException('Category id not match')
        
        cat: Category = Category(**cat_exists)
        # set updated values
        cat.cat_name = category.cat_name
        cat.cat_desp = category.cat_desp
        
        # update
        result = db.find_one_and_update(
            {'cat_id': cat_id}, {'$set': cat.dict()}
        )

        return cat
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        

@router.delete("/category/cat_id/{cat_id}", response_model=DeleteResponse, status_code=status.HTTP_200_OK)
async def delete_category_by_cat_id(cat_id: int):
    log.info("delete category by cat id called")

    try:
        db = get_connection().get_collection(SchemasEnum.CATEGORY.value)

        cat_exists = db.find_one({"cat_id":cat_id, "disabled": False})

        # validate
        if cat_exists is None:
            raise BadAlertException("Category not exists.")
        
        # delete
        result = db.delete_one({"cat_id": cat_id})

        return DeleteResponse(id=cat_id, status="success", desc="Category delete successful.")
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        
@router.get("/category/next_cat_code", response_model=str, status_code=status.HTTP_200_OK)
async def get_next_cat_code():
    log.info("get next cat code called")
    try:
        # db = get_connection().get_collection(SchemasEnum.CATEGORY.value)
        # last_rec_id = db.find_one({}, {"sort": {"cat_id": -1}})
        # last_rec: Category = db.find_one({"_id": last_rec_id['_id']})

        db = get_connection().get_collection(SchemasEnum.SEQUENCES.value)
        
        next_cat_id_rec = db.find_one({'_id': SchemaSequencesEnum.CATEGORY.value})
        next_cat_id = next_cat_id_rec["sequence_value"]
        
        next_cat_code = f"C{next_cat_id:03}"

        return next_cat_code
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        
## category apis closed