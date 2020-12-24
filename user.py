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
        self.food = Resource(user=self, name='food', activity_name='hunting')
        self.wood = Resource(user=self, name='wood', activity_name='chopping')
        self.coal = Resource(user=self, name='coal', activity_name='coal_mining')
        self.metal = Resource(user=self, name='metal', activity_name='metal_mining')
        self.resources = [self.food, self.wood, self.coal, self.metal]

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
            for resource in self.resources:
                resource.set_amount(0)
                resource.set_speed(0)
                resource.set_level(0)

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
