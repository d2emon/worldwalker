import logging
from datetime import datetime
from ..errors import FileServiceError, CrapupError
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
            raise CrapupError("Log fault : Access Failure")
