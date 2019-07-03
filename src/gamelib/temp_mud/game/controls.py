import logging
from ..keys import Keys
from ..services.log import LogService
from ..player.user import User


class Control:
    def __init__(self):
        self.visible = True

    def show(self, visible=True):
        self.visible = visible
        while self.visible:
            self.on_before_render()
            self.render()
            self.visible = False
            self.on_after_render()

    def render(self):
        raise NotImplementedError()

    def on_before_render(self):
        pass

    def on_after_render(self):
        pass


class BufferedControl(Control):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.buffer = game.buffer

    def add_buffer(self, message):
        self.buffer.add(message)

    def show_buffer(self):
        print("".join(self.buffer.show(self.game)))

    def render(self):
        raise NotImplementedError()

    def on_before_render(self):
        self.show_buffer()

    def on_after_render(self):
        self.show_buffer()


class InputControl(BufferedControl):
    def __init__(
        self,
        game,
        on_input=lambda value: None,
    ):
        super().__init__(game=game)
        self.value = None
        self.on_input = on_input

    def render(self):
        raise NotImplementedError()

    def on_after_render(self):
        self.buffer.add(self.value, raw=True)
        self.on_input(self.value)


class TtyControl(BufferedControl):
    def __init__(self, game, tty=0):
        super().__init__(game)
        self.tty = tty

    def show_tty(self):
        raise NotImplementedError()

    def render(self):
        if self.tty == 4:
            self.show_tty()

    def on_before_render(self):
        pass

    def on_after_render(self):
        pass


class ScreenHeader(Control):
    def __init__(self, caption=""):
        super().__init__()
        self.caption = caption

    def render(self):
        print(self.caption)

    def on_before_render(self):
        print("-" * 80)


class ScreenInput(InputControl):
    def __init__(
        self,
        game,
        timer,
        on_input=lambda value: None,
    ):
        super().__init__(
            game=game,
            on_input=on_input
        )
        self.timer = timer

    def render(self):
        self.value = input()
        # self.value = Keys.get_command(self.parser.prompt, 80)

    def on_before_render(self):
        print("Input  ........." + "." * 64)
        self.timer.active = True

    def on_after_render(self):
        self.timer.active = False
        super().on_after_render()


class ScreenTop(TtyControl):
    def show_tty(self):
        # topscr()
        pass

    def on_before_render(self):
        print("Top    ........." + "." * 64)


class ScreenMain(BufferedControl):
    def __init__(self, game):
        super().__init__(game=game)
        self.command = None

    def render(self):
        # self.buffer.add(*self.user.read_messages())
        print(self.command)
        # if self.parser.parse(self.command) is None:
        #     return
        # self.buffer.add(*self.user.read_messages(unique=True))

    def on_before_render(self):
        print("Main   ........." + "." * 64)
        # World.load()

    def on_after_render(self):
        super().on_after_render()
        # World.save()
        print("Render Main")


class ScreenTimer(BufferedControl):
    def __init__(self, game):
        super().__init__(game=game)
        self.__active = False

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        self.show()
        self.__active = value

    def render(self):
        # self.parser.read_messages(*self.user.read_messages(interrupt=self.interrupt))
        self.game.user.on_time()

    def show(self, visible=True):
        return super().show(self.active)

    def __reprint(self):
        self.buffer.break_line = True
        self.buffer.add(Keys.buffer)
        self.buffer.show(self)
        self.buffer.reprint(Keys.reprint())

    def on_before_render(self):
        print("Timer  ........." + "." * 64)
        self.__active = False
        # World.load()

    def on_after_render(self):
        self.__reprint()
        # World.save()
        self.__active = True


class ScreenBottom(TtyControl):
    def show_tty(self):
        # btmscr()
        pass

    def on_before_render(self):
        print("Bottom ........." + "." * 64)
        self.buffer.show(self.game)

    def on_after_render(self):
        self.buffer.show(self.game)
        print("-" * 80)


class CreateUser(InputControl):
    def __init__(self, game):
        super().__init__(game=game)
        self.on_input = self.after_input

        self.add_buffer("Creating character....\n")
        self.add_buffer("\n")
        self.add_buffer("Sex (M/F) : ")
        self.show(True)

    @property
    def data(self):
        return {
            'sex': self.value,
        }

    def render(self):
        self.on_input(Keys.get_sex())

    def after_input(self, value):
        self.value = {
            'm': User.SEX_MALE,
            'f': User.SEX_FEMALE,
        }.get(value)

    def on_after_render(self):
        self.visible = self.value is None
        if self.visible:
            self.buffer.add("M or F")


class FinalMessage(Control):
    dashes = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"

    def __init__(self, message=""):
        super().__init__()
        self.message = message
        self.show(True)

    def render(self):
        print(self.message)

    def on_before_render(self):
        print()
        print(self.dashes)
        print()

    def on_after_render(self):
        print()
        print(self.dashes)
        raise SystemExit(0)


class MainScreen(BufferedControl):
    waiting = True

    def __init__(
        self,
        game,
        user,
    ):
        super().__init__(game=game)
        self.user = user

        # Signals
        self.__active = False
        self.__last_interrupt = None

        self.timer_control = ScreenTimer(game=self.game)

        self.header = ScreenHeader()
        self.command_input = ScreenInput(
            game=game,
            timer=self.timer_control,
            on_input=self.on_input,
        )
        self.top = ScreenTop(game=self.game)
        self.main_control = ScreenMain(game=self.game)
        self.bottom = ScreenBottom(game=self.game)

        self.controls = [
            self.header,
            self.command_input,
            self.top,
            self.main_control,
            self.bottom,
        ]

    @property
    def command(self):
        return self.main_control.command

    @command.setter
    def command(self, value):
        self.main_control.command = value

    def render(self):
        [control.show() for control in self.controls]

    def on_before_render(self):
        # Set caption
        if self.user.visible > 9999:
            self.header.caption = "-csh"
        elif self.user.visible == 0:
            self.header.caption = "   --}}----- ABERMUD -----{{--     Playing as {}".format(self.user.name)

    def on_after_render(self):
        self.visible = True

    def on_input(self, value):
        self.command = value


def show_intro(**kwargs):
    user_id = kwargs.get('user_id')
    name = kwargs.get('name')

    print("Entering Game ....")
    print("Hello {}".format(name))
    LogService.post_system(message="GAME ENTRY: {}[{}]".format(name, user_id))
