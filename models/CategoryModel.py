from pydantic import BaseModel

class Category(BaseModel):
    cat_id: int | None = None
    cat_code: str | None = None
    cat_name: str | None = None
    cat_desp: str | None = None
    disabled: bool | None = None