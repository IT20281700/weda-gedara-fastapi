from pydantic import BaseModel


class ErrorDto(BaseModel):
    status_code: str
    path: str
    message: str


class ValidationError(BaseModel):
    loc: list[str]
    msg: str
    type: str


class UnprocessableErrorDto(BaseModel):
    status_code: str
    path: str
    message: list[ValidationError]


# custom bad alert exception model
class BadAlertException(Exception):
    def __init__(self, description: str):
        self.description = description
