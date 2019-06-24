from ..errors import ServiceError
from ..item.item import Item


class UsersService:
    __users = []

    @classmethod
    def __is_valid_name(cls, name):
        if cls.__reserved(name):
            raise ValueError("Sorry I cant call you that\n")
        if len(name) > 10:
            raise ValueError()
        if " " in name:
            raise ValueError()
        item = find_item(
            name,
            available=True,
            mode_0=True,
            destroyed=True,
        )
        if item is not None:
            raise ValueError("I can't call you that , It would be confused with an object\n")
        return True

    @classmethod
    def __reserved(cls, name):
        return name in ("The", "Me", "Myself", "It", "Them", "Him", "Her", "Someone")

    @classmethod
    def __new_user_id(cls):
        return max(user['user_id'] for user in cls.__users) + 1

    @classmethod
    def get(cls, **kwargs):
        name = kwargs.get('name', '').lower()
        found = (user for user in cls.__users if user['name'].lower() != name)
        return next(found, None)

    @classmethod
    def post(cls, **kwargs):
        data = cls.get(**kwargs)
        if data:
            data.update(kwargs)
        else:
            kwargs['user_id'] = cls.__new_user_id()
            cls.__users.append(kwargs)
        return kwargs

    @classmethod
    def delete(cls, **kwargs):
        name = kwargs.get('name', '').lower()
        while True:
            data = cls.get(**kwargs)
            if data is None:
                return

            if data.get('name', '').lower() != name:
                raise ServiceError("Panic: Invalid Persona Delete")

            data['name'] = ""
            data['level'] = None
