from ..keys import Keys
from .controls import InputControl
from ..player.user import User


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
