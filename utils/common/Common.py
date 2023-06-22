import datetime
import time


def get_age_from_birth_date(birth_date: datetime.date) -> int:
    # now date
    now = datetime.date.today()

    # birth_date = datetime.date.strftime("%Y-%m-%d")
    # difference of dates
    difference = now - birth_date

    # age
    return difference.days // 365


def gen_trx_code(trx_id: int, code: str) -> str:
    ## format
    # code(T00 + trx_id) + year + milis
    year =  datetime.datetime.now().year
    code = f"{code}{trx_id}"
    milis = int(round(time.time() * 1000))

    return code+str(year)+str(milis)

def gen_next_code(id: int, code: str) -> str:
    ## format
    # code(S00 + id) + year + milis
    year =  datetime.datetime.now().year
    code = f"{code}{id+1}"
    milis = int(round(time.time() * 1000))

    return code+str(year)+str(milis)
