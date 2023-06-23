import datetime
from pydantic import BaseModel

from models.CategoryModel import Category

class Stock(BaseModel):
    stock_id: int | None = None
    cat_id: int | None = 0
    stock_code: str | None = 'null'
    name: str | None = 'null'
    desp: str | None = 'null'
    manufacture: str | None = 'null' # supplier
    filled_no_of_units: float | None = 0.0
    sold_no_of_items: float | None = 0.0
    available_no_of_items: float | None = 0.0
    measure_unit: str | None = 'null'
    prev_unit_price: float | None = 0.0
    unit_price: float | None = 0.0
    curr_code: str | None = "LKR"
    filled_datetime: datetime.datetime | None = None
    created_datetime: datetime.datetime | None = None
    updated_datetime: datetime.datetime | None = None
    disabled: bool | None = False


class StockView(Stock):
    category: Category | None = 'null'