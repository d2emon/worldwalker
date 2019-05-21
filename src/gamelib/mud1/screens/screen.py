from ..gmainstubs import clear


class Screen:
    clear_before = True

    @classmethod
    def show(cls, **kwargs):
        if not kwargs.get('visible', False):
            return
        if cls.clear_before:
            clear()

    @classmethod
    def show_message(cls, message):
        print(message)
