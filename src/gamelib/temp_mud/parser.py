def openworld():
    raise NotImplementedError()


def closeworld():
    raise NotImplementedError()


class Buffer:
    def __init__(self):
        self.__sysbuf = ""

    def show(self):
        raise NotImplementedError()

    def add(self, text):
        self.__sysbuf += text


class Screen:
    def __init__(self, tty=0):
        self.tty = tty
        self.parser = Parser()
        self.buffer = Buffer()

        self.__key_buffer = ""

    def top(self):
        if self.tty != 4:
            return
        # topscr()

    def bottom(self):
        self.buffer.show()
        if self.tty != 4:
            return
        # btmscr()

    def get_input(self):
        # sig_alon()
        # key_input(self.parser.prompt)[:80]
        # sig_aloff()
        return self.__key_buffer

    def set_progname(self, *args):
        raise NotImplementedError()

    def send_message(self, user):
        self.bottom()

        self.buffer.show()

        if user.player.visible > 9999:
            self.set_progname(0, "-csh")
        elif user.player.visible == 0:
            self.set_progname(0, "   --}----- ABERMUD -----{--     Playing as {}".format(user.name))

        work = self.get_input()

        self.top()

        self.buffer.add("\001l{}\n\001".format(work))

        self.parser.parse(user, work, self.send_message)


class Parser:
    def __init__(self):
        self.__conversation_flag = 0

    def get_prompt(self, user):
        if self.__conversation_flag == 0:
            prompt = ">"
        elif self.__conversation_flag == 1:
            prompt = "\""
        elif self.__conversation_flag == 2:
            prompt = "*"
        else:
            prompt = "?"

        if user.is_wizard:
            prompt = "----" + prompt
        if user.debug_mode:
            prompt = "#" + prompt

        if user.player.visible:
            prompt = "(" + prompt + ")"
        return prompt

    def reset_conversation_mode(self):
        if self.__conversation_flag:
            self.__conversation_flag = 0
            return True
        return False

    def parse(self, user, work, on_reinput):
        openworld()
        user.read_messages()
        closeworld()

        if work:
            if work == "**" and self.reset_conversation_mode():
                on_reinput(user)
            elif work[0] == "*" and work != "*":
                work = work[1:]
            elif self.__conversation_flag == 1:
                work = "say {}".format(work)
            elif self.__conversation_flag == 2:
                work = "tss {}".format(work)

        if user.mode == 1:
            self.__gamecom(user, work)
        elif work and work.lower != ".q":
            self.__special(user, work)

        user.check_fight()

        return work.lower() == ".q"

    def __gamecom(self, user, action):
        raise NotImplementedError()

    def __special(self, user, action):
        raise NotImplementedError()
