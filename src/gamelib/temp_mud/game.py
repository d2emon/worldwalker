from datetime import datetime
from .bprintf import Buffer
from .errors import CrapupError, ServiceError
from .keys import Keys
from .parser import Parser
from .player.user import User
from .services.log import LogService
from .world import World


class Control:
    def render(self):
        raise NotImplementedError()


class TtyControl(Control):
    def __init__(self, tty=0):
        self.tty = tty

    def show_tty(self):
        raise NotImplementedError()

    def render(self):
        if self.tty == 4:
            self.show_tty()


class ScreenHeader(Control):
    def __init__(self, user, caption=""):
        self.user = user
        self.caption = caption

    def render(self):
        if self.user.visible > 9999:
            self.caption = "-csh"
        elif self.user.visible == 0:
            self.caption = "   --}----- ABERMUD -----{--     Playing as {}".format(self.user.name)
        print(self.caption)


class ScreenInput(Control):
    def __init__(self, on_activate=lambda control: None, on_deactivate=lambda control: None):
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate
        self.value = None

    def render(self):
        self.on_activate(self)
        # self.value = Keys.get_command(self.parser.prompt, 80)
        self.on_deactivate(self)


class ScreenTop(TtyControl):
    def show_tty(self):
        # topscr()
        pass


class ScreenMain(Control):
    def __init__(self, buffer):
        self.buffer = buffer
        self.command = None

    def render(self):
        World.load()
        # self.buffer.add(*self.user.read_messages())
        # if self.parser.parse(self.command) is None:
        #     return
        # self.buffer.add(*self.user.read_messages(unique=True))
        # self.buffer.show()
        World.save()


class ScreenBottom(TtyControl):
    def __init__(self, buffer, tty=0):
        super().__init__(tty)
        self.buffer = buffer

    def show_tty(self):
        # btmscr()
        pass

    def render(self):
        self.buffer.show()
        super().render()
        self.buffer.show()


class CreateUser(Control):
    def __init__(self, buffer, game):
        self.buffer = buffer
        self.value = None
        self.game = game
        self.render()

    def render(self):
        self.buffer.add("Creating character....\n")
        self.buffer.add("\n")
        self.buffer.add("Sex (M/F) : ")

        print(list(self.buffer.show(self.game)))

        # self.value = {
        #     'm': User.SEX_MALE,
        #     'f': User.SEX_FEMALE,
        # }.get(Keys.get_sex())

        self.value = input()
        if self.value is None:
            self.buffer.add("M or F")
            return self.render()


class FinalMessage(Control):
    dashes = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"

    def __init__(self, message):
        self.message = message
        self.render()

    def render(self):
        print()
        print(self.dashes)
        print()
        print(self.message)
        print()
        print(self.dashes)
        raise SystemExit(0)


def show_intro(**kwargs):
    user_id = kwargs.get('user_id')
    name = kwargs.get('name')

    print("Entering Game ....\n")
    print("Hello {}\n".format(name))
    LogService.post_system(message="GAME ENTRY: {}[{}]".format(name, user_id))


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

        self.main_control = ScreenMain(self.buffer)
        self.controls = [
            # ScreenHeader(self.user),
            ScreenInput(
                on_activate=self.on_before_input,
                on_deactivate=self.on_after_input,
            ),
            ScreenTop(),
            self.main_control,
            ScreenBottom(self.buffer),
        ]

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        if self.__active:
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
        print(list(self.parser.start()))
        # for s in self.parser.start():
        #     print(s)
        self.user.in_setup = True

    def create_user(self):
        print("create_user")
        return {
            'sex': CreateUser(self.buffer, self).value
        }

    def play(self):
        try:
            Keys.on()
            self.__start()
            self.main()
        except SystemExit as e:
            return self.on_error(e)
        except CrapupError as e:
            return self.on_finish(e)
        except KeyboardInterrupt:
            return self.on_quit()
        finally:
            Keys.off()

    def main(self):
        while True:
            map(lambda control: control.render(), self.controls)

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
        self.main_control.command = control.value

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
        World.load()

        # self.parser.read_messages(*self.user.read_messages(interrupt=self.interrupt))
        # self.user.on_time()

        World.save()
        Keys.reprint()
        self.__active = True
