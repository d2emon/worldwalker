import logging
import uuid
from games.mud.exceptions import FileServiceError


LOG_LEVEL = logging.INFO

files_logger = logging.getLogger('files')
files_logger.setLevel(LOG_LEVEL)


class FileService:
    logger = files_logger
    filename = None
    connections = dict()
    content = None

    def __init__(self, **query):
        self.query = query
        self.token = None

    def __enter__(self):
        self.token = self.connect(**self.query)
        return self.token

    def __exit__(self, exc_type, exc_value, traceback):
        return self.disconnect(self.token)

    @classmethod
    def __verify_token(cls, token):
        query = cls.connections.get(token)
        if query is None:
            raise FileServiceError("Wrong token")
        return query

    @classmethod
    def connect(cls, **query):
        token = uuid.uuid1()
        cls.logger.debug("fopen(%s, %s) => %s", cls.filename, query, token)

        cls.connections[token] = query

        return token

    @classmethod
    def disconnect(cls, token):
        cls.logger.debug("fclose(%s)", token)
        cls.__verify_token(token)

        del cls.connections[token]

        return True

    @classmethod
    def get_data(cls, token, **kwargs):
        if cls.content is None:
            raise FileServiceError()

        for data in cls.content:
            cls.logger.debug("fscanf(%s, %s)", token, kwargs)
            cls.__verify_token(token)
            yield data

    @classmethod
    def add_line(cls, token, line, **kwargs):
        cls.logger.debug("fprintf(%s, %s, %s)", token, line, kwargs)
        cls.__verify_token(token)

        cls.content.append(line)

        return True

    @classmethod
    def get_line(cls, token, **kwargs):
        if cls.content is None:
            raise FileServiceError()

        for data in cls.content:
            cls.logger.debug("fgets(%s, %s)", token, kwargs)
            cls.__verify_token(token)
            yield data

    @classmethod
    def get_content(cls, token):
        return "\n".join(cls.get_line(token, max_length=128))

    @classmethod
    def truncate(cls, token, new_content=None):
        cls.__verify_token(token)
        cls.content = new_content

    @classmethod
    def execute(cls, token, *args):
        cls.logger.info("execl(%s, %s)", token, [cls.filename, *args])


class LockFileService(FileService):
    LOCK_UN = 0
    LOCK_EX = 1

    @classmethod
    def __set_lock(cls, token, lock):
        """
        INTERRUPTED SYSTEM CALL CATCH

        :return:
        """
        try:
            cls.logger.debug("flock(%s, %s)", token, lock)
            cls.connections[token]['lock'] = lock
        except FileServiceError:
            cls.__set_lock(token, lock)
        return token

    @classmethod
    def connect(cls, **query):
        token = super().connect(**query)
        # NOTE: Always open with R or r+ or w
        cls.__set_lock(token, cls.LOCK_EX)
        return token

    @classmethod
    def disconnect(cls, token):
        cls.__set_lock(token, cls.LOCK_UN)
        return super().disconnect(token)


class TextFileService(LockFileService):
    @classmethod
    def get_content(cls, token):
        return "\n".join(cls.get_line(token, max_length=128))

    @classmethod
    def get_text(cls):
        """

        :return:
        """
        try:
            with cls(permissions='r+') as token:
                return "\n" + cls.get_content(token) + "\n"
        except FileServiceError:
            raise FileServiceError("[Cannot Find -> {}]".format(cls))
