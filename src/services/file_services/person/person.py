from ...errors import CrapupError
from ...utils import test_valid_username


class Person:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = self.validate_username(username)
        self.password = self.validate_password(password)

    @property
    def is_wizard(self):
        return self.user_id in ["wisner"]

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
            raise CrapupError("\nIllegal characters in user name\n")
        if not check_username(value):
            raise ValueError()

        try:
            test_valid_username(value)
        except ValueError as e:
            print(e)
            raise CrapupError("Bye Bye")

        return value
