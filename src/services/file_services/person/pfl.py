from games.mud.exceptions import FileServiceError, MudError
from ..file_service import LockFileService


class Pfl(LockFileService):
    filename = "pfl"
    connections = dict()
    content = []

    @classmethod
    def __encode(cls, user):
        return user

    @classmethod
    def __decode(cls, user):
        return user

    @classmethod
    def clear(cls):
        cls.content = []

    @classmethod
    def add_line(cls, token, line, encoded=True, **kwargs):
        if encoded:
            user = line
        else:
            user = cls.__encode(line)
        super().add_line(token, user, **kwargs)

    @classmethod
    def get_line(cls, token, encoded=True, **kwargs):
        user = super().get_line(token, **kwargs)
        if encoded:
            return user
        else:
            return cls.__decode(user)

    @classmethod
    def add_user(cls, user):
        with cls(permissions="a") as token:
            cls.add_line(token, user, encoded=False)
            return user

    @classmethod
    def del_user(cls, username):
        search = username.lower()
        try:
            with cls(permissions="r+") as token:
                users = cls.get_line(token)
                cls.clear()
                for user in filter(lambda u: cls.__decode(u).username.lower() != search, users):
                    cls.add_line(token, user)
            return True
        except FileServiceError:
            return False

    @classmethod
    def find_user(cls, username):
        try:
            search = username.lower()
            with cls(permissions="r") as token:
                users = cls.get_line(token, encoded=False)
                return list(filter(lambda user: user.username.lower() == search, users))
        except FileServiceError:
            raise MudError("No persona file\n")
