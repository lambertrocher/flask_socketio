import pymongo
from flask_login import UserMixin


class Resource:
    def __init__(self, user, name) -> None:
        self.user = user
        self.name = name

    def set_amount(self, amount):
        self.user.user_collection.update_one(filter={'id': self.user.id}, update={'$set': {'gold': amount}})

    def set_speed(self, amount):
        self.user.user_collection.update_one(filter={'id': self.user.id}, update={'$set': {'mining_speed': amount}})

    def get_amount(self):
        return self.user.user_collection.find_one({'id': self.user.id})['gold']

    def get_speed(self):
        return self.user.user_collection.find_one({'id': self.user.id})['mining_speed']
