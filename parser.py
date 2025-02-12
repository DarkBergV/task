import pymongo
import requests
import json
from dataclasses import dataclass, asdict
from pymongo import MongoClient
from datetime import datetime


url = "https://gist.githubusercontent.com/pakiusdevo/691f51c19d1111816ed7782623ee03e0/raw/c19a0955bd659be7d7c07e92b4f1c116ba9ea301/udata.json"
response = requests.get(url)
data = response.json()
with open("users.json", "w") as json_file:
    json.dump(data, json_file, indent=4)


client = MongoClient("mongodb://localhost:27017")
db = client["users"]
collection = db["users"]


@dataclass
class UserPreferences:
    timezone: str


@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    created_ts: float
    active: bool = True


with open("users.json", "r") as file:
    users = json.load(file)


def get_user_roles(user):
    roles = []

    if user["is_user_admin"]:
        roles.append("admin")
    if user["is_user_manager"]:
        roles.append("manager")
    if user["is_user_tester"]:
        roles.append("tester")
    return roles


for user in users["users"]:

    try:
        user_roles = get_user_roles(user)
        user_preferences = UserPreferences(timezone=user["user_timezone"])
        created_ts = datetime.strptime(
            user["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        ).timestamp()

        mongouser = User(
            username=user["user"],
            password=user["password"],
            roles=user_roles,
            preferences=user_preferences,
            active=user["is_user_active"],
            created_ts=created_ts,
        )

        user_dict = asdict(mongouser)

        collection.insert_one(user_dict)
    except:
        print("rroer")
