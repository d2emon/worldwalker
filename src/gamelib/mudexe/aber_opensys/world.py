from .dummies import DummyGlobals
from ..database.database import WorldDatabase
from ..database.exceptions import LockFileException, NoWorldFileException
from ..aber_gamego import crapup


class NoDatabaseException(Exception):
    pass


class World:
    database = None  # - = not open

    @classmethod
    def open(cls):
        if cls.database is not None:
            return cls.database

        try:
            cls.database = WorldDatabase()

            DummyGlobals.objinfo = cls.database.load_objects()
            DummyGlobals.ublock = cls.database.load_persons()
        except (LockFileException, NoWorldFileException) as message:
            crapup(message)
        finally:
            if not cls.database:
                raise NoDatabaseException()

        return cls.database

    @classmethod
    def close(cls):
        if cls.database is None:
            return

        cls.database.save_objects(DummyGlobals.objinfo)
        cls.database.save_persons(DummyGlobals.ublock)

        cls.database.close()
        cls.database = None
