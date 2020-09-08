import logging
from datetime import datetime
from games.mud.exceptions import FileServiceError, MudError
from .file_service import TextFileService


class LogFile(TextFileService):
    filename = "log_file"
    connections = dict()
    content = []

    @classmethod
    def log(cls, text):
        try:
            with cls(permissions="a") as token:
                cls.add_line(token, "{}:  {}\n".format(datetime.now(), text))
                logging.info(text)
        except FileServiceError:
            # loseme()
            raise MudError("Log fault : Access Failure")
