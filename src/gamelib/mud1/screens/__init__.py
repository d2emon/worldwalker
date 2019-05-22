from services.errors import CrapupError
from .screen import Screen
from .game_over import GameOver
from .game_screen import GameScreen, TestGameScreen
from .main_screen import UserScreen, MainScreen
from .motd import MessageOfTheDay
from .splash import Splash


class RetryError(Exception):
    pass


class LoginScreen(Screen):
    @classmethod
    def validate_username(cls, service):
        def f(username):
            return service.get_validate_username(username)
        return f

    @classmethod
    def process_answer(cls, answer):
        if not answer:
            raise RetryError()

    @classmethod
    def auth(cls, service):
        def wrapper(username):
            def f(password):
                try:
                    return service.get_auth(username, password)
                except PermissionError as e:
                    raise RetryError(e)
            return f
        return wrapper

    @classmethod
    def save_user(cls, service):
        def wrapper(username):
            def f(password):
                try:
                    return service.post_user(username, password)
                except ValueError as e:
                    raise RetryError(e)
            return f
        return wrapper

    @classmethod
    def __set_password(cls, save_callback):
        try:
            return save_callback(cls.input_new_password())
        except ValueError as e:
            cls.show_message(e)
            return cls.__set_password(save_callback)

    @classmethod
    def show(cls, **kwargs):
        """
        The whole login system is called from this

        Get the user name

        :return:
        """
        # super().show(**kwargs)
        service = kwargs.get('service')
        try:
            username = cls.input_username(
                kwargs.get('username'),
                on_enter=cls.validate_username(service),
            )
            if service.get_user(username):
                return cls.input_password(
                    on_enter=cls.auth(service)(username),
                )

            cls.verify_username(
                on_enter=cls.process_answer,
                onusername=username,
            )

            print("Creating new persona...")
            print("Give me a password for this persona")
            # self.quick_start = False
            return cls.input_new_password(on_enter=cls.save_user(service)(username))
        except RetryError as e:
            cls.show_message(e)
            return cls.show()

    @classmethod
    def input_username(cls, value=None, on_enter=lambda value: value):
        if value:
            return value
        print("By what name shall I call you ?")
        value = input("*")[:15].strip()
        on_enter(value)
        return value

    @classmethod
    def input_password(cls, on_enter=lambda value: None, tries=0):
        try:
            print()
            print("This persona already exists, what is the password ?")
            value = input("*")
            print()
            on_enter(value)
            return value
        except RetryError as e:
            cls.show_message(e)
            if tries >= 2:
                raise CrapupError("\nNo!\n\n")
            cls.input_password(on_enter=on_enter, tries=tries + 1)

    @classmethod
    def input_new_password(cls, on_enter=lambda value: None):
        try:
            value = input("*")
            print()
            on_enter(value)
            return value
        except RetryError as e:
            cls.show_message(e)
            cls.input_new_password(on_enter=on_enter)

    @classmethod
    def verify_username(cls, on_enter=lambda value: None, **kwargs):
        # If he/she doesnt exist
        print()
        value = input("Did I get the name right {username} ?".format(**kwargs)).lower()[0] != 'n'
        on_enter(value)
        return value
