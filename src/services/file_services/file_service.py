import logging
import uuid
from ..errors import FileServiceError


class FileService:
    filename = None
    connections = dict()
    content = None

    LOCK_UN = 0
    LOCK_EX = 1

    @classmethod
    def __verify_token(cls, token):
        query = cls.connections.get(token)
        if query is None:
            raise FileServiceError("Wrong token")
        return query

    @classmethod
    def __lock(cls, token, lock):
        logging.debug("flock(%s, %s)", token, lock)
        cls.__verify_token(token)

        cls.connections[token]['lock'] = lock

        return True

    @classmethod
    def __set_lock(cls, token):
        """
        INTERRUPTED SYSTEM CALL CATCH

        :return:
        """
        try:
            cls.__lock(token, cls.LOCK_EX)
        except IOError:
            cls.__set_lock(token)
        return token

    @classmethod
    def connect(cls, lock=False, **query):
        token = uuid.uuid1()
        logging.debug("fopen(%s, %s) => %s", cls.filename, query, token)

        cls.connections[token] = query

        if lock:
            # NOTE: Always open with R or r+ or w
            return cls.__set_lock(token)

        return token

    @classmethod
    def disconnect(cls, token, lock=False):
        logging.debug("fclose(%s)", token)
        cls.__verify_token(token)

        if lock:
            cls.__lock(token, cls.LOCK_UN)

        del cls.connections[token]

        return True

    @classmethod
    def get_data(cls, token, **kwargs):
        if cls.content is None:
            raise FileServiceError()

        for data in cls.content:
            logging.debug("fscanf(%s, %s)", token, kwargs)
            cls.__verify_token(token)
            yield data

    @classmethod
    def add_line(cls, token, line, **kwargs):
        logging.debug("fprintf(%s, %s, %s)", token, line, kwargs)
        cls.__verify_token(token)

        cls.content.append(line)

        return True

    @classmethod
    def get_line(cls, token, **kwargs):
        if cls.content is None:
            raise FileServiceError()

        for data in cls.content:
            logging.debug("fgets(%s, %s)", token, kwargs)
            cls.__verify_token(token)
            yield data


class TextFileService(FileService):
    @classmethod
    def get_content(cls, token):
        return "\n".join(cls.get_line(token, max_length=128))

    @classmethod
    def get_text(cls):
        """

        :return:
        """
        try:
            token = cls.connect(lock=True, permissions='r+')
            text = "\n" + cls.get_content(token) + "\n"
            cls.disconnect(token)
            return text
        except FileServiceError:
            raise FileServiceError("[Cannot Find -> {}]".format(cls))
