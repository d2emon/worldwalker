from games.mud.exceptions import MudError
from games.mud.database.users import User
from .pfl import Pfl


class Person:
    def __init__(self, user_id, username, password="default"):
        self.user_id = user_id
        self.username = self.validate_username(username)
        self.password = self.validate_password(password)
        self.is_new = True

    @property
    def is_wizard(self):
        return self.user_id not in ["wisner"]

    @classmethod
    def validate_password(cls, value):
        if not value:
            raise ValueError()
        if "." in value:
            raise ValueError("Illegal character in password")
        return value

    @classmethod
    def validate_username(cls, value):
        def check_username(username):
            """

            :param username:
            :return:
            """
            for a in username.lower():
                if a > 'z' or a < 'a':
                    return False
            return True

        if not value:
            raise ValueError
        if "." in value:
            raise MudError("\nIllegal characters in user name\n")
        if not check_username(value):
            raise ValueError()

        User.fields['username'](value)

        return value

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'is_wizard': self.is_wizard,
            'is_new': self.is_new,
        }

    def add(self):
        # user = Person(user_id, username, password)
        return Pfl.add_user(self).as_dict()

    @classmethod
    def find(cls, username):
        found = Pfl.find_user(username)
        if len(found) <= 0:
            return None
        user = found[0]
        user.is_new = False
        return found[0].as_dict()

    @classmethod
    def auth(cls, username, password):
        user = Person.find(username)
        if user is None:
            raise PermissionError()
        if password != user['password']:
            raise PermissionError()
        return user

    @classmethod
    def delete(cls, username):
        search = username.lower()
        user = Person.find(search)
        if user is None:
            raise ValueError("\nCannot delete non-existant user")
        return Pfl.del_user(username)
