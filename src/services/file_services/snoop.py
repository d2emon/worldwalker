import logging
from .file_service import LockFileService


class Snoop(LockFileService):
    filename = "snoop/"
    connections = dict()
    content = []

    @classmethod
    def connect(cls, **query):
        super().connect(**query)
        user = query.get('user')
        logging.info("fopen(%s%s)", cls.filename, user)

    @classmethod
    def get_line(cls, token, **kwargs):
        for line in super().get_line(token, **kwargs):
            yield "|{}".format(line)

    @classmethod
    def clear(cls, token):
        cls.truncate(token, [])

    @classmethod
    def view(cls, user):
        with cls.connect(user=user, permissions="r+") as token:
            result = cls.get_content(token)
            cls.clear(token)
        return result
