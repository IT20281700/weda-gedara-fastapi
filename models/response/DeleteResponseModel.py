from pydantic import BaseModel


class DeleteResponse(BaseModel):
    id: str
    status: str
    desc: str