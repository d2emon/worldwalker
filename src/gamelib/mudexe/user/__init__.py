from ..database.database import WorldDatabase
from .exceptions import DuplicateEntryException


class User:
    def __init__(self, name):
        self.name = name
        self.is_on = False
        self.message_id = None
        self.person_id = 0
        self.location_id = 0

    def __str__(self):
        return self.name

    def put_on(self):
        self.is_on = False

        world = WorldDatabase()

        if world.fpbn(self.name) is not None:
            raise DuplicateEntryException()

        self.person_id = world.find_empty_person()
        world.add_person(self.person_id, self)

        self.is_on = True
