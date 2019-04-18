from ..database.world import World
from ..database.models.person import Person
from .exceptions import DuplicateEntryException


class User:
    def __init__(self, name):
        self.name = name
        self.is_on = False
        self.message_id = None
        self.person_id = 0
        self.location_id = 0
        self.last_update = 0
        self.in_setup = False

    def __str__(self):
        return self.name

    @property
    def person(self):
        return Person(self.person_id)

    def put_on(self):
        self.is_on = False

        World.open()

        if Person.fpbn(self.name) is not None:
            raise DuplicateEntryException()

        self.person_id = Person.find_empty_person()
        self.person.add_user(self)

        self.is_on = True

    @property
    def need_update(self):
        messages = self.message_id - self.last_update
        if messages < 0:
            messages = -messages
        return messages >= 10

    def update(self):
        if not self.need_update:
            return

        World.open()
        self.person.pos = self.message_id
        self.last_update = self.message_id
