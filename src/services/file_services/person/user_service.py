from ..file_service import LockFileService


class UserService:
    @classmethod
    def __clear(cls):
        LockFileService.content = []

    @classmethod
    def __add(cls, token, data, **kwargs):
        return LockFileService.add_line(token, data, **kwargs)

    @classmethod
    def __next(cls, token, **kwargs):
        yield from LockFileService.get_line(token, **kwargs)

    @classmethod
    def service_add(cls, user):
        with LockFileService(permissions="r") as token:
            cls.__add(token, user)
            return user

    @classmethod
    def service_get(cls, user_id):
        with LockFileService(permissions="r") as token:
            yield from (u for u in cls.__next(token) if u.username.lower() == user_id)

    @classmethod
    def service_delete(cls, user_id):
        with LockFileService(permissions="r") as token:
            users = [u for u in cls.__next(token) if u.username.lower != user_id]
            cls.__clear()
            for user in users:
                cls.__add(token, user)
            return True
