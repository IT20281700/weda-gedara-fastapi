from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from os import environ as env
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from models.response.CreateResponseModel import CreateResponseModel
from useEnum.Enum import InitializeEnum, SchemaSequencesEnum, SchemasEnum

# logger
from Imports.logger import logging
log = logging.getLogger(__name__.upper())


config = {
    "uri": "mongodb+srv://chamodwedagedaradbuser:chamod@cluster0.0zqvu.mongodb.net/?retryWrites=true&w=majority",
    "db_name": "weda_gedara_db"
}


def get_connection():
    # Create a new client and connect to the server
    client = MongoClient(config["uri"], server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        log.info("Connection successful")
        # get db
        return client.get_database(config["db_name"])
    except Exception as e:
        log.error(e)


oauth_2_schema = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(
    prefix=f"{env['BASE_URL']}"+'/admin',
    tags=['admin'],
    dependencies=[Depends(oauth_2_schema)]
)


@router.put("/init_tables", response_model=CreateResponseModel, status_code=status.HTTP_200_OK)
def admin_init_tables():
    try:
        db = get_connection()
        # check tables were already created
        for tableName in SchemasEnum:
            if tableName.value not in db.list_collection_names():
                # create collections
                db.create_collection(tableName.value)
                log.info(tableName.value+" :: collection created")

        # check and create sequence list
        for sequence in SchemaSequencesEnum:
            if not db[SchemasEnum.SEQUENCES.value].find_one({'_id': sequence.value}):
                db[SchemasEnum.SEQUENCES.value].insert_one(
                    {"_id": sequence.value, "sequence_value": 0},
                )
                log.info(sequence.value+" :: sequence created")

        # success
        log.info("Table and Sequences creation successfull")

        response = CreateResponseModel(
            id=InitializeEnum.INT.value,
            status=InitializeEnum.STRING.value,
            desc=InitializeEnum.STRING.value
        )

        response.id = 999
        response.status = 'success'
        response.desc = 'mongo db collections updated successful.'
        return response
    except Exception as e:
        log.error(e.errors())
        raise HTTPException(status_code=400, detail=f"{e.errors()}")
