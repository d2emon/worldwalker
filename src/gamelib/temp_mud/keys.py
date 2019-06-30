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
    def get_prompt(cls, max_length=None):
        if max_length is None:
            return ""
        return cls.__get_keyboard(max_length)

    @classmethod
    def frobnicate(cls):
        # def data():
        #     yield cls.buffer_prompt("New Level: ", 6)
        #     yield cls.buffer_prompt("New Score: ", 8)
        #     yield cls.buffer_prompt("New Strength: ", 8)
        # return cls.get_input(lambda: data())
        print("frobnicate")
        return None

    @classmethod
    def get_command(cls, prompt, max_length):
        # cls.input_mode = True
        # cls.prompt = prompt
        # cls.buffer_prompt(buffer, message=cls.prompt)

        # buffer.to_show = False
        # cls.buffer = input()[:max_length]
        # print("\n")
        # cls.input_mode = False
        # return cls.buffer
        print("get command", prompt, max_length)
        return None

    @classmethod
    def reprint(cls):
        if cls.input_mode:
            return ""
        return "\n{}{}".format(cls.prompt, cls.buffer)

    # Inputs
    @classmethod
    def get_input(cls, on_input=lambda: ""):
        cls.off()
        value = on_input()
        cls.on()
        return value

    @classmethod
    def get_sex(cls):
        return cls.get_input(lambda: cls.__get_keyboard(2).lower())

    @classmethod
    def system(cls, command):
        return cls.get_input(lambda: cls.__system(command))
