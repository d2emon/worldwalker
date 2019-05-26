"""
Fast File Controller v0.1
"""
import logging
from ..errors import CrapupError, FileServiceError
from ..file_services.file_service import LockFileService


def new_user():
    return [None] * 16


class World(LockFileService):
    OFFSET_MESSAGE_DATA = 0
    OFFSET_USERS = 350
    OFFSET_OBJECTS = 400

    filename = "/usr/tmp/-iy7AM"

    __messages_data = [0, 10]
    __messages = []
    __objects = []
    __users = [new_user() for _ in range(48)]

    @classmethod
    def read(cls, token, offset, block_size):
        if offset == cls.OFFSET_MESSAGE_DATA:
            data = cls.__messages_data
        elif cls.OFFSET_MESSAGE_DATA < offset < cls.OFFSET_OBJECTS:
            data = cls.__messages[offset - cls.OFFSET_MESSAGE_DATA - 1]
        elif offset == cls.OFFSET_OBJECTS:
            data = cls.__objects
        elif offset == cls.OFFSET_USERS:
            data = cls.__users
        else:
            data = None
        # logging.debug("sec_read(%s, %s, %s, %s)", token, data, offset, block_size)
        return data

    @classmethod
    def write(cls, token, data, offset, block_size):
        if offset == cls.OFFSET_MESSAGE_DATA:
            cls.__messages_data = data
        elif cls.OFFSET_MESSAGE_DATA < offset < cls.OFFSET_OBJECTS:
            cls.__messages[offset - cls.OFFSET_MESSAGE_DATA - 1] = data
        elif offset == cls.OFFSET_OBJECTS:
            cls.__objects = data
        elif offset == cls.OFFSET_USERS:
            cls.__users = data
        # logging.debug("sec_write(%s, %s, %s, %s)", token, data, offset, block_size)
        return True

    @classmethod
    def first_message_id(cls, token):
        return cls.read(token, cls.OFFSET_MESSAGE_DATA, 1)[0]

    @classmethod
    def last_message_id(cls, token):
        return cls.read(token, cls.OFFSET_MESSAGE_DATA, 2)[1]

    @classmethod
    def message(cls, token, message_id):
        actnum = message_id * 2 - cls.first_message_id(token)
        return cls.read(token, actnum, 128)

    @classmethod
    def player(cls, player_id):
        return cls.__users[player_id]


class WorldService:
    __token = None  # - = not open

    # External
    __objinfo = None
    __numobs = 1
    __ublock = None

    def __init__(self):
        self.token = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.disconnect()

    @classmethod
    def connect(cls):
        """

        :return:
        """
        if cls.__token is not None:
            return cls.__token

        try:
            cls.__token = World.connect(permissions="r+")
            cls.__objinfo = World.read(cls.__token, 400, 4 * cls.__numobs)
            cls.__ublock = World.read(cls.__token, 350, 16 * 48)
            return cls.__token
        except FileServiceError:
            raise CrapupError("Cannot find World file")

    @classmethod
    def disconnect(cls):
        """

        :return:
        """
        if cls.__token is None:
            return

        World.write(cls.__token, cls.__objinfo, 400, 4 * cls.__numobs)
        World.write(cls.__token, cls.__ublock, 350, 16 * 48)
        World.disconnect(cls.__token)
        cls.__token = None

    @classmethod
    def get_last_message_id(cls):
        return World.last_message_id(cls.__token)

    @classmethod
    def get_player(cls, player_id):
        return World.player(player_id)

    @classmethod
    def get_message(cls, message_id):
        return World.message(cls.__token, message_id)
