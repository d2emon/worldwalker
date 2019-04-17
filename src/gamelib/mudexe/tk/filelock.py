from .dummies import LOCK_UN, LOCK_EX, EINTR, ENOSPC, EHOSTDOWN, EHOSTUNREACH, errno, fopen
from ..gamego import crapup


def openlock(file, perm):
    def intr():
        if unit.fileno.flock(LOCK_EX) is None:
            if errno == EINTR:
                return intr() # INTERRUPTED SYSTEM CALL CATCH

        if errno == ENOSPC:
            crapup("PANIC exit device full\n")
        elif errno in (EHOSTDOWN, EHOSTUNREACH):
            #  ESTALE
            crapup("PANIC exit access failure, NFS gone for a snooze")

        return unit

    unit = fopen(file, perm)

    if unit is None:
        return unit

    # NOTE: Always open with R or r+ or w
    return intr()


def fcloselock(file):
    file.flush()
    file.fileno().flock(LOCK_UN)
    file.close()
