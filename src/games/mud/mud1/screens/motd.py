from .screen import Screen


class MessageOfTheDay(Screen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)
        input(kwargs.get('message'))
        print()
        print()
