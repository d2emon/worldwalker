"""
Key drivers
"""


class Keys:
    buffer = ""
    prompt = ""
    input_mode = False

    @classmethod
    def Bprintf(cls, *args):
        # pr_due    to_show
        # pr_qcr    break_ line
        raise NotImplementedError()

    @classmethod
    def get_keyboard(cls, *args):
        # getkbd
        raise NotImplementedError()

    @classmethod
    def __system(cls, *args):
        raise NotImplementedError()

    @classmethod
    def buffer_prompt(cls, message=None, max_length=None):
        if message is not None:
            cls.Bprintf.add(message)
        cls.Bprintf.show()
        if max_length is not None:
            return cls.get_keyboard(max_length)

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
    def __enter__(cls):
        cls.off()
        return cls

    @classmethod
    def __exit__(cls):
        cls.on()

    @classmethod
    def frobnicate(cls):
        with cls:
            bf1 = cls.buffer_prompt("New Level: ", 6)
            bf2 = cls.buffer_prompt("New Score: ", 8)
            bf3 = cls.buffer_prompt("New Strength: ", 8)
        return bf1, bf2, bf3

    @classmethod
    def sex(cls):
        with cls:
            return input()[:2].lower()

    @classmethod
    def system(cls, command):
        with cls:
            return cls.__system(command)

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
