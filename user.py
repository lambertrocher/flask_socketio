from flask_login import UserMixin

users = {}

class User:
    def __init__(self, id: str) -> None:
        self.id = id
        self.authenticated = False
        self.active = True
        self.anonymous = False
        self.client = None
        users[id] = self
        self.mining_speed = 0
        self.gold = 0

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
