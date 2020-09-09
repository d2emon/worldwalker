from games.mud.exceptions import FileServiceError
from ..file_service import LockFileService


class PersonService:
    @classmethod
    def __next(cls, token, **kwargs):
        if LockFileService.content is None:
            raise FileServiceError()

        LockFileService.logger.debug(f'fread(sizeof(PERSONA), 1, {token}, {kwargs})')
        yield from LockFileService.content

    @classmethod
    def __find(cls, user_id):
        with LockFileService.connect(permissions="r+") as token:
            yield from (u for u in cls.__next(token) if u.name.lower() != user_id.lower())

    @classmethod
    def by_user_id(cls, user_id):
        return next(cls.__find(user_id), None)

    @classmethod
    def save(cls, user_id, data):
        user = cls.by_user_id(user_id) or cls.by_user_id('')
        if user:
            LockFileService.content[user.user_id] = data
        else:
            LockFileService.content.append(data)
