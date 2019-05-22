"""
Program starts Here!

This forms the main loop of the code, as well as calling
all the initialising pieces
"""
from services.errors import CrapupError
from services.mud1 import Mud1Services
from ..gmlnk import quick_start, talker
from ..screens import Splash, LoginScreen, MessageOfTheDay, GameOver


class MudGame:
    def __init__(self, host, username=None):
        self.host = host
        self.service = Mud1Services(self.host)

        self.__username = username
        self.quick_start = bool(self.username)

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = self.service.get_validate_username(value)

    @property
    def show_all(self):
        return not self.quick_start

    def __try_password(self, tries=0):
        try:
            return self.service.get_auth(self.username, LoginScreen.input_password())
        except PermissionError:
            if tries >= 2:
                raise CrapupError("\nNo!\n\n")
            return self.__try_password(tries + 1)

    def __set_password(self):
        try:
            return self.service.post_user(self.username, LoginScreen.input_new_password())
        except ValueError as e:
            LoginScreen.show_message(e)
            return self.__set_password()

    @classmethod
    def game_over(cls, message):
        """
        Exit

        :param message:
        :return:
        """
        GameOver.show_message(message=message)

    def get_user(self):
        return self.service.get_user(self.username)

    def login(self, username=None):
        """
        The whole login system is called from this

        Get the user name

        :return:
        """
        try:
            self.username = LoginScreen.input_username(value=username)

            if self.get_user():
                return self.__try_password()

            LoginScreen.new_user(username=self.username)
            self.quick_start = False
            return self.__set_password()
        except ValueError as e:
            LoginScreen.show_message(e)
            return self.login()

    def play(self):
        """
        The initial routine

        :return:
        """
        print("\n" * 4)
        try:
            Splash.show(
                visible=self.show_all,
                **self.service.get_time(),
            )
            user = self.login(username=self.username)
            MessageOfTheDay.show(
                visible=self.show_all,
                message=self.service.get_message_of_the_day()
            )
            if self.quick_start:
                quick_start(user, self)
            else:
                talker(user, self)
            GameOver.show_message(
                message="Bye Bye"
            )
        except CrapupError as e:
            GameOver.show_message(
                message=e
            )
