"""
Key drivers
"""


class Keys:
    buffer = ""
    prompt = ""
    input_mode = False

    @classmethod
    def __enter__(cls):
        cls.on()
        return cls

    @classmethod
    def __exit__(cls):
        cls.off()

    @classmethod
    def Bprintf(cls, *args):
        raise NotImplementedError()

    @classmethod
    def on(cls):
        # ios = tcgetattr(None)
        # self.save_flags = ios.flags
        # ios.flags = {
        #     "ECHO": True,
        #     "ICANON": True,
        # }
        # tcsetattr(None, TCSANOW, ios)
        pass

    @classmethod
    def off(cls):
        # ios = tcgetattr(None)
        # ios.flags = self.save_flags
        # tcsetattr(None, TCSANOW, ios)
        pass

    @classmethod
    def __system(cls, *args):
        raise NotImplementedError()

    @classmethod
    def __get_keyboard(cls, max_length):
        """
        Getstr() with length limit and filter ctrl

        :param max_length:
        :return:
        """
        return input()[:max_length]

    @classmethod
    def buffer_prompt(cls, message=None, max_length=None):
        if message is not None:
            cls.Bprintf.add(message)
        cls.Bprintf.show()
        if max_length is not None:
            return cls.__get_keyboard(max_length)

    @classmethod
    def frobnicate(cls):
        def data():
            yield cls.buffer_prompt("New Level: ", 6)
            yield cls.buffer_prompt("New Score: ", 8)
            yield cls.buffer_prompt("New Strength: ", 8)
        return cls.get_input(lambda: data())

    @classmethod
    def get_sex(cls):
        return cls.get_input(lambda: cls.__get_keyboard(2).lower())

    @classmethod
    def system(cls, command):
        return cls.get_input(lambda: cls.__system(command))

    @classmethod
    def get_command(cls, prompt, max_length):
        cls.input_mode = True
        cls.prompt = prompt
        cls.buffer_prompt(cls.prompt)

        cls.Bprintf.to_show = False
        cls.buffer = input()[:max_length]
        print("\n")
        cls.input_mode = False
        return cls.buffer

    @classmethod
    def reprint(cls):
        cls.Bprintf.break_line = True
        cls.buffer_prompt()
        if not cls.input_mode and cls.Bprintf.to_show:
            print("\n{}{}".format(cls.prompt, cls.buffer))
        cls.Bprintf.to_show = False

    @classmethod
    def get_input(cls, on_input=lambda: ""):
        cls.off()
        value = on_input()
        cls.on()
        return value
