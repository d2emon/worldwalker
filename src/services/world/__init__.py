"""
Fast File Controller v0.1
"""
import logging
from ..errors import CrapupError, FileServiceError
from ..file_services.file_service import LockFileService


class World(LockFileService):
    OFFSET_MESSAGE_DATA = 0
    OFFSET_USERS = 350
    OFFSET_OBJECTS = 400

    filename = "/usr/tmp/-iy7AM"

    __messages_data = [0, 10]
    __objects = []
    __users = []

    @classmethod
    def read(cls, token, offset, block_size):
        if offset == cls.OFFSET_MESSAGE_DATA:
            data = cls.__messages_data
        elif offset == cls.OFFSET_OBJECTS:
            data = cls.__objects
        elif offset == cls.OFFSET_USERS:
            data = cls.__users
        else:
            data = None
        logging.debug("sec_read(%s, %s, %s, %s)", token, data, offset, block_size)
        return data

    @classmethod
    def write(cls, token, data, offset, block_size):
        if offset == cls.OFFSET_MESSAGE_DATA:
            cls.__messages_data = data
        elif offset == cls.OFFSET_OBJECTS:
            cls.__objects = data
        elif offset == cls.OFFSET_USERS:
            cls.__users = data
        logging.debug("sec_write(%s, %s, %s, %s)", token, data, offset, block_size)
        return True

    @classmethod
    def first_message_id(cls, token):
        return cls.read(token, 0, 1)[0]

    @classmethod
    def last_message_id(cls, token):
        return cls.read(token, 0, 2)[1]


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
