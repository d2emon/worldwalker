from .screen import Screen
from .main_screen import UserScreen, MainScreen
from.game_screen import GameScreen, TestGameScreen


class Splash(Screen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)
        print()
        print("                         A B E R  M U D")
        print()
        print("                  By Alan Cox, Richard Acott Jim Finnis")
        print()
        print(kwargs.get('created'))
        print(kwargs.get('elapsed'))


class LoginScreen(Screen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)

    @classmethod
    def input_username(cls):
        print("By what name shall I call you ?")
        return input("*")[:15].strip()

    @classmethod
    def input_password(cls):
        print()
        print("This persona already exists, what is the password ?")
        value = input("*")
        print()
        return value

    @classmethod
    def verify_username(cls, **kwargs):
        print()
        return input("Did I get the name right {username} ?".format(**kwargs)).lower()[0] != 'n'

    @classmethod
    def new_user(cls):
        print("Creating new persona...")
        print("Give me a password for this persona")

    @classmethod
    def input_new_password(cls):
        value = input("*")
        print()
        return value


class MessageOfTheDay(Screen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)
        input(kwargs.get('message'))
        print()
        print()


class GameOver(Screen):
    clear_before = False

    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)
        print()
        print(kwargs.get('message'))
        print()
        input("Hit Return to Continue...")
