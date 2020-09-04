import pymongo

from config.config import mongo_uri
from .user_cache import UserCache


class DataDriver:
    """ A datadriver API class """

    def __init__(self, dbname="botmojo", user_cache_size=2500):
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[dbname]

        self.users = self.db["users"]
        self.usercache = UserCache(user_cache_size)

    def get_user(self, user_id: str, use_cache=True) -> object:
        if self.usercache.exists(user_id) and use_cache:
            return self.usercache.get(user_id)
        data = self.users.find({"_id": user_id})
        try:
            data = data[0]
            self.usercache.add(user_id, data)
            return data
        except IndexError:
            return None

    def create_user(self, user_id: str, user_data: dict) -> bool:
        if not self.get_user(user_id):
            data = {"_id": user_id, **user_data}
            self.users.insert_one(data)
            self.usercache.add(user_id, data)

            return True
        return False

    def update_user(self, user_id: str, keys: dict) -> bool:
        if not self.get_user(user_id, False):
            return self.create_user(user_id, keys)

        new_values = {"$set": keys}
        self.users.update_one({"_id": user_id}, new_values)
        return True

    def delete_user(self, user_id: str):
        self.usercache.pop(user_id)
        if self.get_user(user_id):
            self.users.delete_one({"_id": user_id})
            return True
        return False
