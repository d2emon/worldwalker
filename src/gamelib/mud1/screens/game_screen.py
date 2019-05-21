from .screen import Screen


class GameScreen(Screen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)
        if not kwargs.get('show_intro', True):
            return
        print("The Hallway")
        print("You stand in a long dark hallway, which echoes to the tread of your")
        print("booted feet. You stride on down the hall, choose your masque and enter the")
        print("worlds beyond the known......")
        print()


class TestGameScreen(Screen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)
        print("Entering Test Version")
