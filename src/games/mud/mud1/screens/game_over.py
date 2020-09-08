from .screen import Screen


class GameOver(Screen):
    clear_before = False

    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)
        print()
        print(kwargs.get('message'))
        print()
        input("Hit Return to Continue...")
        raise SystemExit()
