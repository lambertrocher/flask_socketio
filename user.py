import pymongo
from flask_login import UserMixin

users = {}


class User:
    def __init__(self, id: str, app) -> None:
        self.id = id
        self.authenticated = False
        self.active = True
        self.anonymous = False
        self.client = None

        self.mongo_client = pymongo.MongoClient(
            f"mongodb+srv://admin:{app.config['MONGO_PASSWD']}@cluster0.soder.mongodb.net/admin?retryWrites=true&w=majority"
        )
        self.db = self.mongo_client.app
        self.user_collection = self.db.users

        if not self.user_collection.count({'id': self.id}):
            user = {
                "id": self.id,
                "mining_speed": 0,
                "gold": 0,
            }
            self.user_collection.insert_one(user)

        users[id] = self

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.anonymous

    def set_gold(self, amount):
        self.user_collection.update_one(filter={'id': self.id}, update={'$set': {'gold': amount}})

    def set_mining_speed(self, amount):
        self.user_collection.update_one(filter={'id': self.id}, update={'$set': {'mining_speed': amount}})

    def get_gold(self):
        return self.user_collection.find_one({'id': self.id})['gold']

    def get_mining_speed(self):
        return self.user_collection.find_one({'id': self.id})['mining_speed']

    @staticmethod
    def get(user_id):
        return users.get(user_id)

    @staticmethod
    def users():
        return users
