import uuid


class FileService:
    connections = dict()

    @classmethod
    def connect(cls, **query):
        token = uuid.uuid1()
        cls.connections[token] = query
        print("\tfopen", query, token)
        return token

    @classmethod
    def openlock(cls, **query):
        print("\topenlock", query)
        return cls.connect(**query)

    @classmethod
    def verify_token(cls, token):
        query = cls.connections.get(token)
        if query is None:
            raise Exception("Wrong token")
        return query

    @classmethod
    def disconnect(cls, token):
        print("\tfclose", token)
        cls.verify_token(token)
        del cls.connections[token]

    @classmethod
    def get_data(cls, token, **kwargs):
        cls.verify_token(token)
        print("\tfscanf", token, kwargs)
        yield None

    @classmethod
    def get_line(cls, token, **kwargs):
        cls.verify_token(token)
        print("\tfgets", token, kwargs)
        yield None


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
    def get_content(cls, token):
        return "\n".join(cls.get_line(token, max_length=128))

    @classmethod
    def get_text(cls):
        """

        :return:
        """
        try:
            token = cls.openlock(permissions='r+')
        except FileNotFoundError:
            raise FileNotFoundError("[Cannot Find -> {}]".format(cls))

        text = "\n" + cls.get_content(token) + "\n"
        cls.disconnect(token)
        return text
