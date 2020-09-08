from games.mud.exceptions import FileServiceError
from .file_service import TextFileService


class MotD(TextFileService):
    filename = "motd"
    connections = dict()
    content = [
        "Message of the day",
    ]

    @classmethod
    def get_message(cls):
        try:
            # list the message of the day
            return cls.get_text()
        except FileServiceError as e:
            return e
