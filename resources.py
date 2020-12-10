import pymongo
from flask_login import UserMixin


class Resource:
    def __init__(self, user, name) -> None:
        self.user = user
        self.name = name

    def set_amount(self, value):
        self.user.user_collection.update_one(filter={'id': self.user.id}, update={'$set': {f'{self.name}.amount': value}})

    def set_speed(self, value):
        self.user.user_collection.update_one(filter={'id': self.user.id}, update={'$set': {f'{self.name}.speed': value}})

    def get_amount(self):
        return self.user.user_collection.find_one({'id': self.user.id})[self.name].get('amount', 0)

    def get_speed(self):
        return self.user.user_collection.find_one({'id': self.user.id})[self.name].get('speed', 0)
