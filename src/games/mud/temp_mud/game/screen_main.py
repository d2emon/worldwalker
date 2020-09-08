from .controls import BufferedControl, ScreenTimer, ScreenHeader, ScreenInput, ScreenTop, ScreenMain, ScreenBottom


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
