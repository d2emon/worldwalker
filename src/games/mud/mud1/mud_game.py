"""
Program starts Here!

This forms the main loop of the code, as well as calling
all the initialising pieces
"""
from games.mud.exceptions import MudError, RetryError, GameStopped
from services import auth, logger, stats
from ..mudexe import GameGo
from .options import OPTIONS
from .screens import Splash, LoginScreen, MessageOfTheDay, MainScreen, GameScreen, GameOver


class MudGame:
    def __init__(self, host, username=None):
        self.__username = username
        self.__host_id = host.host_id
        self.quick_start = bool(self.username)

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = auth.validate(self.__host_id, 0, 'username', value)

    @property
    def show_all(self):
        return not self.quick_start

    def on_auth(self, username, password):
        try:
            return auth.get_auth(self.__host_id, 0, username, password)
        except PermissionError as e:
            raise RetryError(e)

    def on_save(self, username, password):
        try:
            return auth.post_user(self.__host_id, 0, 0, username, password)
        except ValueError as e:
            raise RetryError(e)

    def on_old_password(self, username, password):
        try:
            auth.get_auth(self.__host_id, 0, username, password)
        except PermissionError as e:
            raise RetryError(e)

    def on_new_password(self, new_password):
        try:
            auth.validate(self.__host_id, 0, 'password', new_password)
        except ValueError as e:
            raise RetryError(e)

    def on_change_password(self, username, old_password, new_password, verify):
        if verify != new_password:
            raise RetryError("\nNo!")
        auth.put_password(self.__host_id, 0, username, old_password, new_password)

    def play(self):
        """
        The initial routine

        :return:
        """
        print("\n" * 4)
        try:
            Splash.show(
                visible=self.show_all,
                **stats.get_time(),
            )
            user = LoginScreen.show(
                service=auth,
                username=self.username,

                on_username=lambda value: auth.validate(self.__host_id, 0, 'username', value),
                on_password=self.on_auth,
                on_load=lambda username: auth.get_user(self.__host_id, 0, username),
                on_save=self.on_save,
            )
            MessageOfTheDay.show(
                visible=self.show_all,
                message=stats.get_message_of_the_day()
            )
            logger.post("Game entry by {} : UID {}".format(user['username'], user['user_id']))
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
                    on_username=lambda username: auth.get_user(self.__host_id, 0, username),
                    on_old_password=lambda password: self.on_old_password(user['username'], password),
                    on_new_password=self.on_new_password,
                    on_change_password=lambda *args: self.on_change_password(user['username'], *args),
                    on_edit_user=lambda *args: auth.put_user(self.__host_id, 0, 0, *args),
                    on_delete_user=lambda username: auth.delete_user(self.__host_id, 0, username),
                )
            GameOver.show_message(
                message="Bye Bye"
            )
        except MudError as e:
            GameOver.show_message(
                message=e
            )
        except GameStopped as e:
            GameOver.show_message(
                message=e
            )
