from pydantic import BaseModel


class CreateResponseModel(BaseModel):
    id: str
    status: str
    desc: str
