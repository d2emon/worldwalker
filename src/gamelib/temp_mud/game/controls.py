from ..keys import Keys
from ..services.log import LogService
from ..player.user import User


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
        # World.load()
        # self.buffer.add(*self.user.read_messages())
        # if self.parser.parse(self.command) is None:
        #     return
        # self.buffer.add(*self.user.read_messages(unique=True))
        # self.buffer.show()
        # World.save()
        print("Render Main")


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
    def __init__(self, game):
        self.buffer = game.buffer
        self.value = None
        self.game = game

        self.buffer.add("Creating character....\n")
        self.buffer.add("\n")
        self.buffer.add("Sex (M/F) : ")

        self.render()

    def render(self):
        while True:
            print("".join(self.buffer.show(self.game)))
            self.value = {
                'm': User.SEX_MALE,
                'f': User.SEX_FEMALE,
            }.get(Keys.get_sex())

            if self.value is not None:
                return
            self.buffer.add("M or F")


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


class MainScreen(Control):
    def __init__(
        self,
        buffer,
        user,
        on_before_input=lambda control: None,
        on_after_input=lambda control: None,
    ):
        self.main_control = ScreenMain(buffer)
        self.controls = [
            ScreenHeader(user),
            ScreenInput(
                on_activate=on_before_input,
                on_deactivate=on_after_input,
            ),
            ScreenTop(),
            self.main_control,
            ScreenBottom(buffer),
        ]

    @property
    def command(self):
        return self.main_control.command

    @command.setter
    def command(self, value):
        self.main_control.command = value

    def render(self):
        # while True:
        for _ in range(5):
            print(self.controls)
            # map(lambda control: control.render(), self.controls)


def show_intro(**kwargs):
    user_id = kwargs.get('user_id')
    name = kwargs.get('name')

    print("Entering Game ....")
    print("Hello {}".format(name))
    LogService.post_system(message="GAME ENTRY: {}[{}]".format(name, user_id))
