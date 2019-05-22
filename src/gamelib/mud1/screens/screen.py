import logging


class Screen:
    clear_before = True

    @classmethod
    def getty(cls):
        """
        This isnt used on unix

        :return:
        """
        logging.debug("getty()")

    @classmethod
    def clear(cls):
        """
        This isnt used on unix

        :return:
        """
        logging.debug("cls()")
        print("\n" * 24)

    @classmethod
    def show(cls, **kwargs):
        if not kwargs.get('visible', False):
            return
        if cls.clear_before:
            cls.clear()

    @classmethod
    def show_message(cls, message):
        print(message)
