"""
Fast File Controller v0.1
"""
from .consts import *
from .sec import sec_write, sec_read
from .exceptions import LockFileException


class Database:
    def __init__(self, filename, permissions):
        self.filename = filename
        self.permissions = permissions
        self.unit = True
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
