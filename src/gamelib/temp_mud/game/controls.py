from ..keys import Keys


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
