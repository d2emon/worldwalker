from games.mud.exceptions import RetryError
from .screen import Screen


class UserScreen(Screen):
    @classmethod
    def show_user(cls, **kwargs):
        on_username = kwargs.get('on_username', lambda value: value)

        person = cls.input_username(on_enter=on_username)
        cls.show_data(person)
        cls.input_wait()

    @classmethod
    def edit_user(cls, **kwargs):
        user_id = kwargs.get('user_id')
        username = kwargs.get('username')
        on_username = kwargs.get('on_username', lambda value: value)
        on_edit_user = kwargs.get('on_edit_user', lambda *args: None)

        person = cls.input_username(on_enter=on_username)
        if person is None:
            person = {
                'user_id': user_id,
                'username': username,
                'password': 'default'
            }
        cls.show_data(person)
        try:
            return on_edit_user(
                cls.input_field(label="Name:", value=person['username']),
                cls.input_field(label="Password:", value=person['password']),
            )
        except ValueError as e:
            cls.show_message(message=e)

    @classmethod
    def show_data(cls, person):
        """
        for show user and edit user

        :return:
        """
        if person is None:
            print()
            print("No user registered in that name")
            print()
            print()
            return
        print()
        print()
        print("User Data For {username}".format(**person))
        print()
        print("Name:{username}".format(**person))
        print("Password:{password}".format(**person))

    @classmethod
    def input_username(cls, on_enter=lambda value: value):
        cls.before_data()
        value = input("\nUser Name:")[:79]
        return on_enter(value)

    @classmethod
    def input_wait(cls):
        print()
        input("Hit Return...\n")

    @classmethod
    def input_field(cls, **kwargs):
        try:
            value = kwargs.get('value')
            new_value = input("{}(Currently {} ):".format(kwargs.get('label'), kwargs.get('value')))[:128]
            if not new_value:
                return value
            if new_value[0] == ".":
                return value
            if "." in new_value:
                raise ValueError("\nInvalid Data Field\n")
            return new_value
        except ValueError as e:
            cls.show_message(message=e)
            return cls.input_field(**kwargs)

    @classmethod
    def before_data(cls, **kwargs):
        cls.show(**kwargs)

    @classmethod
    def show_edit(cls, **kwargs):
        user = kwargs.get('user')
        print()
        print("Editing : {username}".format(**user))
        print()


class MainScreen(UserScreen):
    @classmethod
    def on_select(cls, option, **kwargs):
        try:
            if option is None:
                raise ValueError()
            option(**kwargs)
        except ValueError:
            cls.show_message(message="Bad Option")
            cls.show(**kwargs)

    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)

        options = kwargs.get('options', dict())
        print("Welcome To AberMUD II [Unix]")
        print()
        print()
        print("Options")
        print()
        print("1]  Enter The Game")
        print("2]  Change Password")
        print()
        print()
        print("0] Exit AberMUD")
        print()
        print()
        if kwargs.get('admin'):
            print("4] Run TEST game")
            print("A] Show persona")
            print("B] Edit persona")
            print("C] Delete persona")
        print()
        print()
        print("Select > ")

        cls.input_option(on_enter=lambda answer: cls.on_select(options.get(answer), **kwargs))

    @classmethod
    def change_password(cls, **kwargs):
        on_old_password = kwargs.get('on_old_password', lambda value: value)
        on_new_password = kwargs.get('on_new_password', lambda value: value)
        on_change_password = kwargs.get('on_change_password', lambda *args: None)

        try:
            old_password = cls.input_old_password(on_enter=on_old_password)
        except PermissionError:
            return cls.show_message(message="\nIncorrect Password")

        print()
        print("New Password")
        new_password = cls.input_new_password(on_enter=on_new_password)
        if cls.input_verify_password() != new_password:
            return cls.show_message(message="\nNo!")

        on_change_password(old_password, new_password)
        cls.show_message(message="Changed")

    @classmethod
    def delete_user(cls, **kwargs):
        on_username = kwargs.get('on_username', lambda value: value)
        on_delete_user = kwargs.get('on_edit_user', lambda *args: None)

        person = cls.input_username(on_enter=on_username)
        try:
            on_delete_user(person['username'])
        except ValueError as e:
            MainScreen.show_message(message=e)

    @classmethod
    def input_option(cls, on_enter=lambda value: value):
        value = input()[:2].lower()
        return on_enter(value)

    @classmethod
    def input_old_password(cls, on_enter=lambda value: value):
        print()
        value = input("Old Password")
        return on_enter(value)

    @classmethod
    def input_new_password(cls, on_enter=lambda value: value):
        try:
            value = input("*")
            print()
            return on_enter(value)
        except RetryError as e:
            cls.show_message(message=e)
            return cls.show()

    @classmethod
    def input_verify_password(cls, on_enter=lambda value: value):
        print()
        print("Verify Password")
        value = input("*")
        print()
        return on_enter(value)
