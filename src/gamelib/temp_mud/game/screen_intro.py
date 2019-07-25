from ..services.log import LogService
from .controls import Control


class IntroMessage(Control):
    def __init__(self, user_id=None, name=""):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.show(True)

    def render(self):
        print("Entering Game ....")
        print("Hello {}".format(self.name))
        LogService.post_system(message="GAME ENTRY: {}[{}]".format(self.name, self.user_id))
