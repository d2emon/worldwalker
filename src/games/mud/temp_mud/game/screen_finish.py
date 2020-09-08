from .controls import Control


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
