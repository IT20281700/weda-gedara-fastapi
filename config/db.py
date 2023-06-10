db = {
    "chamod@gmail.com": {
        "userId": 1,
        "email": "chamod@gmail.com",
        "full_name": "Chamod Ishankha",
        "hashed_password": "$2b$12$alDi8k3BWacU6sRYQTY4i.7WN.6mKlbv4oqWQqHHfAw7a4Hg8FDRS",
        "disabled": False
    },
    "chamod1@gmail.com": {
        "userId": 2,
        "email": "chamod1@gmail.com",
        "full_name": "Chamod Ishankha",
        "hashed_password": "$2b$12$alDi8k3BWacU6sRYQTY4i.7WN.6mKlbv4oqWQqHHfAw7a4Hg8FDRS",
        "disabled": False
    },
}

from pymongo import MongoClient

conn = MongoClient()