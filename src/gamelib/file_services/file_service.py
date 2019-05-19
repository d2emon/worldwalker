import uuid


class FileService:
    filename = None
    connections = dict()

    LOCK_EX = 1

    @classmethod
    def connect(cls, **query):
        token = uuid.uuid1()
        cls.connections[token] = query
        print("\t>>>\tfopen", cls.filename, query, token)
        return token

    @classmethod
    def try_lock(cls, token):
        """
        INTERRUPTED SYSTEM CALL CATCH

        :return:
        """
        try:
            cls.lock(token, cls.LOCK_EX)
        except IOError:
            cls.try_lock(token)
        return token

    @classmethod
    def connect_lock(cls, **query):
        # NOTE: Always open with R or r+ or w
        token = cls.connect(**query)
        return cls.try_lock(token)

    @classmethod
    def verify_token(cls, token):
        query = cls.connections.get(token)
        if query is None:
            raise FileNotFoundError("Wrong token")
        return query

    @classmethod
    def disconnect(cls, token):
        print("\t>>>\tfclose", token)
        cls.verify_token(token)
        del cls.connections[token]

    @classmethod
    def get_data(cls, token, **kwargs):
        cls.verify_token(token)
        print("\t>>>\tfscanf", token, kwargs)
        yield None

    @classmethod
    def get_line(cls, token, **kwargs):
        cls.verify_token(token)
        print("\t>>>\tfgets", token, kwargs)
        return None

    @classmethod
    def add_line(cls, token, line, **kwargs):
        cls.verify_token(token)
        print("\t>>>\tfprintf", token, line, kwargs)
        return None

    @classmethod
    def lock(cls, token, lock):
        print("\t>>>\tflock", token, lock)
        cls.verify_token(token)


class TextFileService(FileService):
    content = None

    @classmethod
    def get_line(cls, token, **kwargs):
        super().get_line(token, **kwargs)
        if cls.content is None:
            raise FileNotFoundError()
        for s in cls.content:
            yield s

    @classmethod
    def add_line(cls, token, line, **kwargs):
        super().add_line(token, line, **kwargs)
        if cls.content is None:
            raise FileNotFoundError()
        cls.content.append(line)

    @classmethod
    def get_content(cls, token):
        return "\n".join(cls.get_line(token, max_length=128))

    @classmethod
    def get_text(cls):
        """

        :return:
        """
        try:
            token = cls.connect_lock(permissions='r+')
        except FileNotFoundError:
            raise FileNotFoundError("[Cannot Find -> {}]".format(cls))

        text = "\n" + cls.get_content(token) + "\n"
        cls.disconnect(token)
        return text
