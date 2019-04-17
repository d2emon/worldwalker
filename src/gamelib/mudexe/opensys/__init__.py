"""
Fast File Controller v0.1
"""
from ..blib import sec_read
from ..gamego import crapup
from ..tk.filelock import openlock, fcloselock


class World:
    file = None  # - = not open

    @classmethod
    def openworld(cls):
        if cls.file is not None:
            return cls.file

        cls.file = openlock("/usr/tmp/-iy7AM", "r+")

        if cls.file is None:
            crapup("Cannot find World file")

        sec_read(cls.file, objinfo, 400, 4 * numobs)
        sec_read(file, ublock, 350, 16 * 48)
        return file

    @classmethod
    def closeworld(cls):
        if cls.file is None:
            return cls.file

        sec_read(cls.file, objinfo, 400, 4 * numobs)
        sec_read(cls.file, ublock, 350, 16 * 48)

        fcloselock(cls.file)

        cls.file = None
