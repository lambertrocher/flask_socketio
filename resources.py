from functools import partialmethod


class Resource:
    def __init__(self, user, name, activity_name) -> None:
        self.user = user
        self.name = name
        self.activity_name = activity_name

    def get_property(self, property):
        return self.user.user_collection.find_one({'id': self.user.id})[self.name].get(property, 0)

    def set_property(self, value, property):
        self.user.user_collection.update_one(filter={'id': self.user.id}, update={'$set': {f'{self.name}.{property}': value}})

    get_amount = partialmethod(get_property, property='amount')
    get_speed = partialmethod(get_property, property='speed')
    get_level = partialmethod(get_property, property='level')

    set_amount = partialmethod(set_property, property='amount')
    set_speed = partialmethod(set_property, property='speed')
    set_level = partialmethod(set_property, property='level')

    def to_json(self):
        return {
            "name": self.name,
            "activity_name": self.activity_name,
            "amount": self.get_amount(),
            "speed": self.get_speed(),
            "level": self.get_level()
        }
