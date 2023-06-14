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
