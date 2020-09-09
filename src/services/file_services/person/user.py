from games.mud.database import validators
from .user_service import UserService


class User(UserService):
    validators = {
        'username': [
            validators.validate_required(),
            validators.validate_characters(
                '.',
                message="Illegal character in username",
            ),
            validators.validate_az(),
            validators.validate_user(),
        ],
        'password': [
            validators.validate_required(),
            validators.validate_characters(
                '.',
                message="Illegal character in password",
            ),
        ],
    }
    __wizards = [
        'd2emon',
    ],

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password', 'default')
        self.is_new = True

    @property
    def is_wizard(self):
        return self.user_id in self.__wizards

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'is_new': self.is_new,
            'is_wizard': self.is_wizard,
        }

    @classmethod
    def validate(cls, field, value):
        validation = cls.validators.get(field, [])
        return all(v(value) for v in validation)

    def validate_all(self):
        fields = {
            'username': self.username,
            'password': self.password,
        }
        return all(self.validate(field, value) for field, value in fields.items())

    def __check_password(self, password):
        return self.password == password

    @classmethod
    def by_username(cls, username):
        user = cls.service_get(username.lower())
        if user is not None:
            user.is_new = False
        return user

    def auth(self, password):
        if not self.__check_password(password):
            raise PermissionError()
        return self

    def update(self, **kwargs):
        self.username = kwargs.get('username', self.username)
        self.password = kwargs.get('password', self.password)
        return self

    def add(self):
        self.validate_all()
        return self.service_add(self)

    def delete(self):
        return self.service_delete(self.username.lower())

    def save(self):
        self.delete()
        return self.add()
