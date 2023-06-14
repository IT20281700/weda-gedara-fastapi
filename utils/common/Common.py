import datetime


def get_age_from_birth_date(birth_date: datetime.date) -> int:
    # now date
    now = datetime.date.today()

    # birth_date = datetime.date.strftime("%Y-%m-%d")
    # difference of dates
    difference = now - birth_date

    # age
    return difference.days // 365
