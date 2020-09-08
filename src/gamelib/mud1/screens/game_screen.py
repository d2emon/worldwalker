from .screen import Screen


class GameScreen(Screen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)

        on_run = kwargs.get('on_run', lambda: None)
        if kwargs.get('show_intro', True):
            print("The Hallway")
            print("You stand in a long dark hallway, which echoes to the tread of your")
            print("booted feet. You stride on down the hall, choose your masque and enter the")
            print("worlds beyond the known......")
            print()
        return on_run()


class TestGameScreen(Screen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)

        print("Entering Test Version")
