from ..aber_opensys.dummies import DummyGlobals
from .consts import *
from .sec import sec_write, sec_read
from .exceptions import LockFileException, NoWorldFileException, WorldFullException


class Database:
    def __init__(self, filename, permissions):
        self.filename = filename
        self.permissions = permissions
        self.unit = "UNIT"
        self.error = None

    def close(self):
        pass

    def flush(self):
        pass

    @property
    def fileno(self):
        return self.unit

    def lock(self, unit, lock):
        return None

    def read(self, pos, max_len):
        return sec_read(self, pos, max_len)

    def write(self, block, pos, max_len):
        sec_write(self, pos, max_len)


class Lockable(Database):
    def __init__(self, filename, permissions):
        super().__init__(filename, permissions)

        # NOTE: Always open with R or r+ or w
        self.set_lock()

    def set_lock(self):
        if self.unit is None:
            return

        if self.lock(self.fileno, LOCK_EX) is None:
            if self.error == EINTR:
                return self.set_lock()  # INTERRUPTED SYSTEM CALL CATCH

        if self.error == ENOSPC:
            raise LockFileException("PANIC exit device full\n")
        elif self.error in (EHOSTDOWN, EHOSTUNREACH):
            #  ESTALE
            raise LockFileException("PANIC exit access failure, NFS gone for a snooze")

    def close(self):
        self.flush()
        self.lock(self.fileno, LOCK_UN)
        super().close()


class WorldDatabase(Lockable):
    __FILENAME = "/usr/tmp/-iy7AM"
    __PERMISSIONS = "r+"

    __OBJECTS_OFFSET = 400
    __OBJECTS_LENGTH = 4 * DummyGlobals.numobs

    __PERSONS_OFFSET = 350
    __PERSONS_LENGTH = 16 * 48

    def __init__(self):
        super().__init__(self.__FILENAME, self.__PERMISSIONS)
        if self.unit is None:
            raise NoWorldFileException()

    def load_objects(self):
        return self.read(self.__OBJECTS_OFFSET, self.__OBJECTS_LENGTH)

    def load_persons(self):
        return self.read(self.__PERSONS_OFFSET, self.__PERSONS_LENGTH)

    def save_objects(self, objects):
        self.write(objects, self.__OBJECTS_OFFSET, self.__OBJECTS_LENGTH)

    def save_persons(self, persons):
        self.write(persons, self.__PERSONS_OFFSET, self.__PERSONS_LENGTH)

    def fpbn(self, username):
        return None

    def find_empty_person(self):
        for person_id in range(DummyGlobals.maxu):
            if not pname(person_id):
                return person_id
        raise WorldFullException()

    def add_person(self, person_id, person):
        pname(person_id).value = person.name
        setploc(person_id, person.location_id)
        setppos(person_id, None)
        setplev(person_id, 1)
        setpvis(person_id, 0)
        setpstr(person_id, None)
        setpwpn(person_id, None)
        setpsex(person_id, 0)
