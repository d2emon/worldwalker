from gamelib.mudexe.temp.exceptions import CrapupException


class DuplicateEntryException(CrapupException):
    def __init__(self):
        super().__init__("You are already on the system - you may only be on once at a time")
