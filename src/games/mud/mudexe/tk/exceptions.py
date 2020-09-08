from gamelib.mudexe.temp.exceptions import CrapupException


class WorldUnavailableException(CrapupException):
    def __init__(self):
        super().__init__("Sorry AberMUD is currently unavailable")
