from games.mud.exceptions import RetryError, MudError
from .screen import Screen


class LoginScreen(Screen):
    @classmethod
    def show(cls, **kwargs):
        """
        The whole login system is called from this

        Get the user name

        :return:
        """
        # super().show(**kwargs)
        on_username = kwargs.get('on_username', lambda value: value)
        on_password = kwargs.get('on_password', lambda *args: False)
        on_load = kwargs.get('on_load', lambda *args: None)
        on_save = kwargs.get('on_save', lambda *args: args)
        try:
            username = cls.input_username(kwargs.get('username'), on_enter=on_username)
            if on_load(username):
                return cls.input_password(on_enter=lambda password: on_password(username, password))

            cls.verify_username(username=username)

            print("Creating new persona...")
            print("Give me a password for this persona")
            # self.quick_start = False
            return cls.input_new_password(on_enter=lambda password: on_save(username, password))
        except RetryError as e:
            cls.show_message(message=e)
            return cls.show()

    @classmethod
    def input_username(cls, value=None, on_enter=lambda value: value):
        if value:
            return value
        print("By what name shall I call you ?")
        value = input("*")[:15].strip()
        return on_enter(value)

    @classmethod
    def input_password(cls, on_enter=lambda value: value, tries=0):
        try:
            print()
            print("This persona already exists, what is the password ?")
            value = input("*")
            print()
            return on_enter(value)
        except RetryError as e:
            cls.show_message(message=e)
            if tries >= 2:
                raise MudError("\nNo!\n\n")
            cls.input_password(on_enter=on_enter, tries=tries + 1)

    @classmethod
    def input_new_password(cls, on_enter=lambda value: value):
        try:
            value = input("*")
            print()
            return on_enter(value)
        except RetryError as e:
            cls.show_message(message=e)
            cls.input_new_password(on_enter=on_enter)

    @classmethod
    def verify_username(cls, **kwargs):
        # If he/she doesnt exist
        print()
        value = input("Did I get the name right {username} ?".format(**kwargs)).lower()[0] != 'n'
        if not value:
            raise RetryError()
        return value
