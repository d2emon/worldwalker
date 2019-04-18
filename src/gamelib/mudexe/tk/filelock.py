from ..aber_gamego import crapup
from ..database.database import Lockable


def openlock(file, perm):
    unit = None
    try:
        unit = Lockable(file, perm)
    except IOError as message:
        crapup(message)
    return unit


def fcloselock(file):
    file.close()
