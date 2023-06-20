# User class mapper
def userEntity(item) -> dict:
    return {
        "user_id": item["user_id"],
        "user_type": item["user_type"],
        "first_name": item["first_name"],
        "last_name": item["last_name"],
        "birth_date": item["birth_date"],
        "gender": item["gender"],
        "email": item["email"],
        "mobile": item["mobile"],
        "address": item["address"],
        "addr_no": item["addr_no"],
        "zip_code": item["zip_code"],
        "state": item["state"],
        "city": item["city"],
        "disabled": item["disabled"],
        "last_login": item["last_login"],
        "login_time": item["login_time"]
    }


# User class list mapper
def userListEntity(entity) -> list:
    return [userEntity(item) for item in entity]


# Category class mapper
def categoryEntity(item) -> dict:
    return {
        "cat_id": item["cat_id"],
        "cat_code": item["cat_code"],
        "cat_name": item["cat_name"],
        "cat_desp": item["cat_desp"],
        "disabled": item["disabled"]
    }

# Category class list mapper
def categoryListEntity(entity) -> list:
    return [categoryEntity(item) for item in entity]
