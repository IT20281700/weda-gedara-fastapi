from pydantic import BaseModel

class Category(BaseModel):
    cat_id: int | None = 'null'
    cat_code: str | None = 'null'
    cat_name: str | None = 'null'
    cat_desp: str | None = 'null'
    disabled: bool | None = False