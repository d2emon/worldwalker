from .screen import Screen


class Splash(Screen):
    @classmethod
    def show(cls, **kwargs):
        cls.getty()
        super().show(**kwargs)
        print()
        print("                         A B E R  M U D")
        print()
        print("                  By Alan Cox, Richard Acott Jim Finnis")
        print()
        print(kwargs.get('created'))
        print(kwargs.get('elapsed'))
