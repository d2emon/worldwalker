from .user import User
from .world import World


class Buffer:
    def __init__(self):
        self.__sysbuf = ""
        makebfr()

    def show(self):
        raise NotImplementedError()

    def add(self, text):
        self.__sysbuf += text


class Screen:
    def __init__(self, username, tty=0):
        self.tty = tty

        self.__key_buffer = ""

        self.user = User(username)
        self.buffer = Buffer()
        self.parser = Parser(self.user)

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

    def send_message(self):
        self.bottom()

        self.buffer.show()

        if self.user.player.visible > 9999:
            self.set_progname(0, "-csh")
        elif self.user.player.visible == 0:
            self.set_progname(0, "   --}----- ABERMUD -----{--     Playing as {}".format(self.user.name))

        work = self.get_input()

        self.top()

        self.buffer.add("\001l{}\n\001".format(work))

        self.parser.parse(work, self.send_message)

    def main(self):
        self.buffer.show()
        self.send_message()
        self.parser.read_messages(False)
        self.buffer.show()


class Parser:
    def __init__(self, user):
        self.user = user

        self.__conversation_flag = 0
        self.__mode = 0

        self.__special(self.user, ".g")
        self.user.in_setup = True

    @property
    def prompt(self):
        if self.__conversation_flag == 0:
            prompt = ">"
        elif self.__conversation_flag == 1:
            prompt = "\""
        elif self.__conversation_flag == 2:
            prompt = "*"
        else:
            prompt = "?"

        if self.user.is_wizard:
            prompt = "----" + prompt
        if self.user.debug_mode:
            prompt = "#" + prompt

        if self.user.player.visible:
            prompt = "(" + prompt + ")"
        return prompt

    def reset_conversation_mode(self):
        if self.__conversation_flag:
            self.__conversation_flag = 0
            return True
        return False

    def parse(self, work, on_reinput):
        World.load()
        self.read_messages()

        if work:
            if work == "**" and self.reset_conversation_mode():
                on_reinput()
            elif work[0] == "*" and work != "*":
                work = work[1:]
            elif self.__conversation_flag == 1:
                work = "say {}".format(work)
            elif self.__conversation_flag == 2:
                work = "tss {}".format(work)

        if self.__mode == 1:
            self.__gamecom(self.user, work)
        elif work and work.lower != ".q":
            self.__special(self.user, work)

        self.user.check_fight()

        return work.lower() == ".q"

    def __gamecom(self, user, action):
        raise NotImplementedError()

    def __special(self, user, action):
        action = action.lower()
        if action[0] != ".":
            return False
        action = action[1:]
        if action == "g":
            self.__mode = 1
            user.start_game()
        else:
            print("\nUnknown . option\n")
        return True

    def read_messages(self, to_read=True):
        self.user.read_messages(to_read)
        World.save()
