import logging
from datetime import datetime
from .file_service import TextFileService


class LogFile(TextFileService):
    filename = "log_file"
    connections = dict()
    content = []

    @classmethod
    def log(cls, text):
        token = cls.connect(lock=True, permissions="a")
        cls.add_line(token, "{}:  {}\n".format(datetime.now(), text))
        logging.info(text)
        cls.disconnect(token)
