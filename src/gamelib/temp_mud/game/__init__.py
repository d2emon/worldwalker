from datetime import datetime
from ..bprintf import Buffer
from ..errors import CrapupError, ServiceError
from ..keys import Keys, without_keys
from ..parser import Parser
from ..player.user import User
# from .world import World
from .screen_create import CreateUser
from .screen_finish import FinalMessage
from .screen_intro import IntroMessage
from .screen_main import MainScreen


class Game:
    def __init__(self, user_id, username, tty=0):
        username = "The " + username if username == "Phantom" else username
        self.user_id = user_id
        self.tty = tty

        IntroMessage(
            user_id=user_id,
            name=username,
        )

        # Signals
        self.__last_interrupt = None

        self.user = User(username)
        self.user.get_new_user = self.create_user

        self.buffer = Buffer()
        self.parser = Parser(self.user)

        self.main_screen = MainScreen(
            self,
            self.user,
        )

    @property
    def interrupt(self):
        time = datetime.now()
        if not self.__last_interrupt or (time - self.__last_interrupt).total_seconds() <= 2:
            return False
        self.__last_interrupt = time
        return True

    # Game flow
    @without_keys
    def play(self):
        try:
            self.on_start()
            return self.main_screen.show()
        except SystemExit as e:
            return self.on_error(e)
        except CrapupError as e:
            return self.on_finish(e)
        except KeyboardInterrupt:
            return self.on_quit()

    def buffer_prompt(self, message=None, max_length=None):
        self.buffer.add(message)
        self.buffer.show(self)
        return Keys.get_prompt(max_length)

    def create_user(self):
        return CreateUser(self).data

    # Events
    def on_error(self, error):
        print(error)
        # self.user.loose()
        raise SystemExit(255)

    def on_finish(self, message):
        self.buffer.show(self)
        self.buffer.to_show = False
        # So we dont get a prompt after the exit

        FinalMessage(message)

    def on_quit(self):
        print("^C\n")
        # if self.user.in_fight:
        #     return

        # self.user.loose()
        self.on_finish("Byeeeeeeeeee  ...........")

    def on_start(self):
        try:
            # World.load()
            # self.buffer.add(*self.user.read_messages(reset_after_read=True))
            # World.save()
            pass
        except ServiceError:
            raise CrapupError("Sorry AberMUD is currently unavailable")

        self.__debug_user()
        self.user.reset_position()
        self.__debug_user()
        self.__debug_list(self.user.start())
        self.__debug_user()
        self.user.in_setup = True
        self.__debug_user()

    # Debug
    def __debug_user(self):
        self.user.log_debug()

    @classmethod
    def __debug_list(cls, text):
        # logging.debug(text)
        print("".join(text))
