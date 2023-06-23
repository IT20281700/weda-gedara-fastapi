
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError

from os import environ as env
from Security.AuthService import get_current_active_user, oauth_2_schema
from config.db import get_connection
from models.StockModel import Stock, StockView

from models.TransactionModel import Transaction
from models.error.ErrorModel import BadAlertException
from models.response.CreateResponseModel import CreateResponseModel
from models.response.DeleteResponseModel import DeleteResponse
from models.response.ResponseTemplateModes import stockEntity, stockListEntity
from useEnum.Enum import Code, SchemaSequencesEnum, SchemasEnum, TrxDescriptions, TrxSign
from utils.common.Common import gen_next_code, gen_trx_code
from utils.common.SequenceGenerator import get_next_sequence_value


# logger
from Imports.logger import getLogger
log = getLogger(__name__)

router = APIRouter(
    prefix=f"{env['BASE_URL']}"+'/stock',
    tags=['stocks'],
    dependencies=[Depends(oauth_2_schema), Depends(get_current_active_user)]
)


## stocks controller
## stocks apis
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def add_new_stock(stock: Stock):
    log.info("add new stock called")
    # get db connection
    db = get_connection()
    try:
        # dto validations
        if (stock.stock_code == '' or stock.stock_code == 'null'):
            raise BadAlertException('Stock code is required')
        if (stock.name == '' or stock.name == 'null'):
            raise BadAlertException('Item name is required.')
        if (stock.measure_unit == '' or stock.measure_unit == 'null'):
            raise BadAlertException('Stock measure unit is required.')
        
        ## validate stock code is already exists
        stock_exists = db.get_collection(
            SchemasEnum.STOCK.value).find_one({"stock_code": stock.stock_code})
        if stock_exists:
            raise BadAlertException("Stock already exists by inserted stock code.")

        # generate sequence and insert to dto
        stock.stock_id = get_next_sequence_value(
            SchemasEnum.SEQUENCES.value, SchemaSequencesEnum.STOCK.value, db)

        stock.created_datetime = datetime.datetime.now()
        stock.updated_datetime = datetime.datetime.now() 

        ## generate create transaction record
        trx: Transaction = Transaction()
        trx.trx_id = get_next_sequence_value(
            SchemasEnum.SEQUENCES.value, SchemaSequencesEnum.TRANSACTION.value, db)
        trx.code = gen_trx_code(trx.trx_id, Code.TRANSACTION.value)
        trx.reference = stock.stock_code
        trx.trx_desp = TrxDescriptions.STOCK_CREATE.value
        trx.manufacture = stock.manufacture
        trx.measure_unit = stock.measure_unit
        trx.curr_code = stock.curr_code
        trx.created_datetime = datetime.datetime.now()
        
        ## save all
        s_result = db[SchemasEnum.STOCK.value].insert_one(dict(stock))
        t_result = db[SchemasEnum.TRANSACTION.value].insert_one(dict(trx))

        return CreateResponseModel(id=str(stock.stock_id), status="success", desc="Item creation successful")
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        

@router.get('/all', response_model=list[StockView], status_code=status.HTTP_200_OK)
async def get_all_stocks():
    log.info("get all stocks called")
    db = get_connection()
    try:
        collection = db.get_collection(SchemasEnum.STOCK.value)
        stock_list: list[StockView] = stockListEntity(collection.find({"disabled": False}))
        return stock_list
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        

@router.get('/stock_id/{stock_id}', response_model=StockView, status_code=status.HTTP_200_OK)
async def get_stock_by_stock_id(stock_id: int):
    log.info("get stock by stock id called")
    db = get_connection()
    try:
        coll = db.get_collection(SchemasEnum.STOCK.value)

        s_exists = coll.find_one({"stock_id": stock_id, "disabled": False})

        # validation
        if s_exists is None:
            raise BadAlertException("Stock not exists.")
        
        return stockEntity(s_exists)
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        

@router.put("/stock_id/{stock_id}", response_model=StockView, status_code=status.HTTP_200_OK)
async def update_stock_by_stock_id(stock_id: int, stock: Stock):
    log.info("update stock by stock id called")
    db = get_connection()
    try:
        coll = db.get_collection(SchemasEnum.STOCK.value)

        s_exists = coll.find_one({"stock_id": stock_id, "disabled": False})

        # validate
        if s_exists is None:
            raise BadAlertException("Stock not exists")
        # dto validation
        if (stock.cat_id == 0):
            raise BadAlertException("Category is required field.")
        if (stock.name == '' or stock.name == 'null'):
            raise BadAlertException("Item name is required field.")
        if (stock.measure_unit == '' or stock.measure_unit == 'null'):
            raise BadAlertException("Measurement unit is required field.")
        if (stock.curr_code == '' or stock.curr_code == 'null'):
            raise BadAlertException("Currency code is required field.")
        

        u_stock: Stock = Stock(**s_exists)
        # set updated values
        u_stock.cat_id = stock.cat_id
        u_stock.name = stock.name
        u_stock.measure_unit = stock.measure_unit
        u_stock.curr_code = stock.curr_code
        u_stock.desp = stock.desp
        u_stock.manufacture = stock.manufacture
        u_stock.updated_datetime = datetime.datetime.now()

        # update
        result: StockView = stockEntity(
            coll.find_one_and_update(
            {"stock_id": stock_id}, 
            {"$set": u_stock.dict()},
            return_document=True
        )
        )

        return stockEntity(result)
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        

@router.delete("/stock_id/{stock_id}", response_model=DeleteResponse, status_code=status.HTTP_200_OK)
async def delete_stock_by_stock_id(stock_id: int):
    log.info("delete stock by stock id called")
    db = get_connection()
    try:
        # validate
        if not db[SchemasEnum.STOCK.value].find_one({"stock_id": stock_id}):
            raise BadAlertException("Stock not exists")
        
        # delete
        result = db[SchemasEnum.STOCK.value].delete_one({"stock_id": stock_id})

        return DeleteResponse(id=stock_id, status="success", desc="Stock Deleted Success")
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")

        

@router.get("/next_stock_code", response_model=str, status_code=status.HTTP_200_OK)
async def get_next_cat_code():
    log.info("get next cat code called")
    try:
        db = get_connection().get_collection(SchemasEnum.SEQUENCES.value)
        
        id = db.find_one({'_id': SchemaSequencesEnum.STOCK.value})
        s_id = id["sequence_value"]
        
        s_code = gen_next_code(s_id, Code.STOCK.value)

        return s_code
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        