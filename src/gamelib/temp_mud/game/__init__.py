from datetime import datetime
from ..bprintf import Buffer
from ..errors import CrapupError, ServiceError
from ..keys import Keys
from ..parser import Parser
from ..player.user import User
# from .world import World
from .controls import show_intro, CreateUser, ScreenTop, ScreenInput, ScreenMain, ScreenBottom, FinalMessage, MainScreen


class Game:
    def __init__(self, user_id, username, tty=0):
        self.user_id = user_id
        if username == "Phantom":
            username = "The " + username
        self.tty = tty

        show_intro(
            user_id=user_id,
            name=username,
        )

        # Signals
        self.__active = False
        self.__caption = ""
        self.__last_interrupt = None

        self.user = User(username)
        self.user.get_new_user = self.create_user

        self.buffer = Buffer()
        self.parser = Parser(self.user)

        self.main_screen = MainScreen(
            self.buffer,
            self.user,
            on_before_input=self.on_before_input,
            on_after_input=self.on_after_input,
        )

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        self.on_timer()
        self.__active = value

    @property
    def interrupt(self):
        time = datetime.now()
        if not self.__last_interrupt or (time - self.__last_interrupt).total_seconds() <= 2:
            return False
        self.__last_interrupt = time
        return True

    # Game flow
    def __start(self):
        try:
            # World.load()
            # self.buffer.add(*self.user.read_messages(reset_after_read=True))
            # World.save()
            pass
        except ServiceError:
            raise CrapupError("Sorry AberMUD is currently unavailable")

        self.user.reset_position()
        for s in self.parser.start():
            print(s)
        self.user.in_setup = True

    def create_user(self):
        return {
            'sex': CreateUser(self).value
        }

    def play(self):
        try:
            Keys.on()
            self.__start()
            self.main_screen.render()
        except SystemExit as e:
            return self.on_error(e)
        except CrapupError as e:
            return self.on_finish(e)
        except KeyboardInterrupt:
            return self.on_quit()
        finally:
            Keys.off()

    def __finish(self, message):
        self.buffer.show(self)
        self.buffer.to_show = False
        # So we dont get a prompt after the exit

        FinalMessage(message)

    # Events
    def on_before_input(self, control):
        self.active = True

    def on_after_input(self, control):
        self.active = False
        self.buffer.add_input(control.value)
        self.main_screen.command = control.value

    def on_error(self, error):
        print(error)
        # self.user.loose()
        raise SystemExit(255)

    def on_finish(self, error):
        self.__finish(error)

    def on_quit(self):
        print("^C\n")
        # if self.user.in_fight:
        #     return

        # self.user.loose()
        self.__finish("Byeeeeeeeeee  ...........")

    def on_timer(self):
        if not self.active:
            return

        self.__active = False
        # World.load()
        # self.parser.read_messages(*self.user.read_messages(interrupt=self.interrupt))
        self.user.on_time()

        self.__reprint()
        # World.save()
        self.__active = True

    def __reprint(self):
        self.buffer.break_line = True

        self.buffer.add(Keys.buffer)
        self.buffer.show(self)

        self.buffer.reprint(Keys.reprint())

    def buffer_prompt(self, message=None, max_length=None):
        self.buffer.add(message)
        self.buffer.show(self)
        return Keys.get_prompt(max_length)
