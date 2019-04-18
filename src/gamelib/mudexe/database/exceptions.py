class LockFileException(IOError):
    pass


class NoDatabaseException(IOError):
    pass


class NoWorldFileException(NoDatabaseException):
    def __init__(self):
        super().__init__("Cannot find World file")


class WorldFullException(Exception):
    def __init__(self):
        super().__init__("\nSorry AberMUD is full at the moment")
