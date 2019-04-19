from .database import Lockable
from .models.message import Message as MessageModel
from .models.object import MudObject
from .models.person import Person
from .exceptions import NoWorldFileException, NoDatabaseException, WorldFullException

from gamelib.services.message import Message


class WorldDatabase(Lockable):
    __filename = "/usr/tmp/-iy7AM"
    __permissions = "r+"

    def __init__(self):
        super().__init__(self.__filename, self.__permissions)

    def load_model(self, model):
        model.items = self.read(model.offset, model.length)

    def save_model(self, model):
        self.write(model.items, model.offset, model.length)

    def load_start(self):
        return Message.first_id

    def load_end(self):
        return Message.last_id


class World:
    database = None  # - = not open

    objects = MudObject
    persons = Person
    messages = MessageModel

    @classmethod
    def is_open(cls):
        if cls.database is None:
            return False
        if cls.database.unit is None:
            return False
        return True

    @classmethod
    def open(cls):
        if cls.is_open():
            return cls.database

        cls.database = WorldDatabase()
        if not cls.is_open():
            raise NoWorldFileException()

        cls.objects.load(cls.database)
        cls.persons.load(cls.database)

        if not cls.is_open():
            raise NoDatabaseException()

        return cls.database

    @classmethod
    def close(cls):
        if not cls.is_open():
            return

        cls.database.save_model(cls.objects)
        cls.database.save_model(cls.persons)

        cls.database.close()

    @classmethod
    def load_message(cls, message_id):
        return Message.get(message_id)
