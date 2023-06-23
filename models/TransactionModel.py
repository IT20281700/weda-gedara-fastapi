import datetime
from pydantic import BaseModel

class Transaction(BaseModel):
    trx_id: int | None = None
    code: str | None = None
    reference: str | None = None
    trx_desp: str | None = False
    manufacture: str | None = None
    trx_sign: str | None = None # plus/minus
    qty: float | None = 0.0
    unit_price: float | None = 0.0
    discounts: float | None = 0.0
    amount: float | None = 0.00
    measure_unit: str | None = None
    curr_code: str | None = "LKR"
    accounting: bool | None = False
    created_datetime: datetime.datetime | None = None
    disabled: bool | None = False