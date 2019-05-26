"""
Key drivers
"""


class Tc:
    __echo = True
    __i_canon = True

    @classmethod
    def get_attr(cls):
        return {
            'ECHO': cls.__echo,
            'ICANON': cls.__i_canon,
        }

    @classmethod
    def set_attr(cls, **kwargs):
        cls.__echo = kwargs.get('ECHO', cls.__echo)
        cls.__i_canon = kwargs.get('ICANON', cls.__i_canon)


class Key:
    MODE_OUTPUT = 0
    MODE_INPUT = 1

    __save_flag = None

    __mode = MODE_OUTPUT
    __prompt = ""
    __buffer = ""

    is_finished = False
    show_prompt = False

    @classmethod
    def connect(cls):
        """

        :return:
        """
        cls.show_prompt = False

        flags = Tc.get_attr()
        cls.save_flag = flags
        Tc.set_attr(
            ECHO=False,
            ICANON=False,
        )

    @classmethod
    def disconnect(cls):
        """

        :return:
        """
        Tc.set_attr(**cls.__save_flag)

    @classmethod
    def reprint(cls):
        """

        :return:
        """
        if cls.__mode == cls.MODE_INPUT and cls.show_prompt:
            print()
            print("{}{}".format(cls.__prompt, cls.__buffer), end="")
        cls.show_prompt = False

    @classmethod
    def get_input(cls, prompt, max_length, on_input=lambda prompt: None):
        """

        :param on_input:
        :param prompt:
        :param max_length:
        :return:
        """
        cls.__mode = cls.MODE_INPUT
        cls.__prompt = prompt
        on_input(prompt)
        cls.show_prompt = False
        cls.__buffer = input()[:max_length]
        cls.__mode = cls.MODE_OUTPUT
        return cls.__buffer
