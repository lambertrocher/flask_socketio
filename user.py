from resources import Resource
from resources import Resource
from resources import Resource
from resources import Resource
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
        self.food = Resource(user=self, name='food')
        self.wood = Resource(user=self, name='wood')
        self.coal = Resource(user=self, name='coal')
        self.metal = Resource(user=self, name='metal')

        self.mongo_client = pymongo.MongoClient(
            f"mongodb+srv://admin:{app.config['MONGO_PASSWD']}@cluster0.soder.mongodb.net/admin?retryWrites=true&w=majority"
        )
        self.db = self.mongo_client.app
        self.user_collection = self.db.users

        if not self.user_collection.count({'id': self.id}):
            user = {
                "id": self.id,
            }
            self.user_collection.insert_one(user)
            self.food.set_amount(0)
            self.food.set_speed(0)
            self.wood.set_amount(0)
            self.wood.set_speed(0)
            self.coal.set_amount(0)
            self.coal.set_speed(0)
            self.metal.set_amount(0)
            self.metal.set_speed(0)

        users[id] = self

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.anonymous

    @staticmethod
    def get(user_id):
        return users.get(user_id)

    @staticmethod
    def users():
        return users
