from ...errors import FileServiceError, CrapupError
from ..file_service import LockFileService


class Uaf(LockFileService):
    filename = "uaf"
    connections = dict()
    content = []

    PCTL_GET = 0
    PCTL_FIND = 1

    @classmethod
    def connect(cls, **query):
        try:
            return super().connect(**query)
        except FileServiceError:
            raise CrapupError("Cannot access UAF\n")

    @classmethod
    def get_line(cls, token, **kwargs):
        if cls.content is None:
            raise FileServiceError()

        for data in cls.content:
            cls.logger.debug("fread(sizeof(PERSONA), 1, %s, %s)", token, kwargs)
            cls.__verify_token(token)
            yield data

    @classmethod
    def get_content(cls, token):
        return "\n".join(cls.get_line(token, max_length=128))

    @classmethod
    def __control(cls, name, action):
        token = cls.connect(permissions="r+")
        search = name.lower()
        for person_id, person in enumerate(cls.get_line(token)):
            if person.name.lower() != search:
                continue
            if action == cls.PCTL_GET:
                cls.disconnect(token)
                return person
            elif action == cls.PCTL_FIND:
                return token, person_id
        cls.disconnect(token)
        return None

    @classmethod
    def find(cls, name):
        return cls.__control(name, cls.PCTL_GET)

    @classmethod
    def save(cls, name, person):
        found = cls.__control(name, cls.PCTL_FIND)
        if found is None:
            found = cls.__control('', cls.PCTL_FIND)
            if found is None:
                cls.content.append(person)
                return
        token, person_id = found
        cls.content[person_id] = person
        cls.disconnect(token)
