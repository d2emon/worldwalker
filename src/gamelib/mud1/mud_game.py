"""
Program starts Here!

This forms the main loop of the code, as well as calling
all the initialising pieces
"""
from services.errors import CrapupError, RetryError
from services.mud1 import Mud1Services
from ..mudexe import GameGo
from .options import OPTIONS
from .screens import Splash, LoginScreen, MessageOfTheDay, MainScreen, GameScreen, GameOver


class MudGame:
    def __init__(self, host, username=None):
        self.service = Mud1Services(host.host_id)

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

    def on_auth(self, username, password):
        try:
            return self.service.get_auth(username, password)
        except PermissionError as e:
            raise RetryError(e)

    def on_save(self, username, password):
        try:
            return self.service.post_user(username, password)
        except ValueError as e:
            raise RetryError(e)

    def on_old_password(self, username, password):
        try:
            self.service.get_auth(username, password)
        except PermissionError as e:
            raise RetryError(e)

    def on_new_password(self, new_password):
        try:
            self.service.get_validate_password(new_password)
        except ValueError as e:
            raise RetryError(e)

    def on_change_password(self, username, old_password, new_password, verify):
        if verify != new_password:
            raise RetryError("\nNo!")
        self.service.put_password(username, old_password, new_password)

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
            user = LoginScreen.show(
                service=self.service,
                username=self.username,

                on_username=self.service.get_validate_username,
                on_password=self.on_auth,
                on_load=self.service.get_user,
                on_save=self.on_save,
            )
            MessageOfTheDay.show(
                visible=self.show_all,
                message=self.service.get_message_of_the_day()
            )
            self.service.post_log("Game entry by {} : UID {}".format(user['username'], user['user_id']))
            if self.quick_start:
                GameScreen.show(
                    show_intro=False,
                    on_run=lambda: GameGo("   --}----- ABERMUD -----{--    Playing as ", user).play(),
                )
            else:
                MainScreen.show(
                    options=OPTIONS,
                    user=user,
                    admin=user['is_wizard'],

                    on_run=lambda: GameGo("   --{----- ABERMUD -----}--      Playing as ", user).play(),
                    on_username=lambda username: self.service.get_user(username),
                    on_old_password=lambda password: self.on_old_password(user['username'], password),
                    on_new_password=self.on_new_password,
                    on_change_password=lambda *args: self.on_change_password(user['username'], *args),
                    on_edit_user=self.service.put_user,
                    on_delete_user=self.service.delete_user,
                )
            GameOver.show_message(
                message="Bye Bye"
            )
        except CrapupError as e:
            GameOver.show_message(
                message=e
            )
