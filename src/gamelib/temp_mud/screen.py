from .buffer import Buffer
from .errors import CrapupError, ServiceError
from .parser import Parser
from .player.user import User
from .world import World


class Screen:
    def __init__(self, username, tty=0):
        self.__program_name = None
        self.tty = tty

        self.__key_buffer = ""

        self.user = User(username)
        self.buffer = Buffer()
        self.parser = Parser(self.user)
        self.user.get_new_user = self.get_new_user

        try:
            World.load()
            # if self.user.player_id >= maxu:
            #     raise Exception("\nSorry AberMUD is full at the moment\n")
            self.buffer.add(*self.user.read_messages(reset_after_read=True))
            World.save()
        except ServiceError:
            raise CrapupError("Sorry AberMUD is currently unavailable")

        self.user.reset_position()
        self.parser.start()
        self.user.in_setup = True

    @property
    def program_name(self):
        return self.__program_name

    @program_name.setter
    def program_name(self, value):
        raise NotImplementedError()

    def top(self):
        if self.tty != 4:
            return
        # topscr()

    def bottom(self):
        self.buffer.show()
        if self.tty != 4:
            return
        # btmscr()

    # Tk
    def __get_input(self):
        # sig_alon()
        value = Keys.get_command(self.parser.prompt, 80)
        # sig_aloff()
        return value

    def get_command(self):
        self.bottom()

        self.buffer.show()

        if self.user.visible > 9999:
            self.program_name = "-csh"
        elif self.user.visible == 0:
            self.program_name = "   --}----- ABERMUD -----{--     Playing as {}".format(self.user.name)

        work = self.__get_input()

        self.top()

        self.buffer.add("\001l{}\n\001".format(work), raw=True)

        World.load()
        self.buffer.add(*self.user.read_messages())

        if self.parser.parse(work) is None:
            return self.get_command()

    def get_new_user(self):
        self.buffer.add("Creating character....\n")
        self.buffer.add("\n")
        self.buffer.add("Sex (M/F) : ")
        self.buffer.show()

        sex = {
            'm': User.SEX_MALE,
            'f': User.SEX_FEMALE,
        }.get(Keys.sex())

        if sex is None:
            self.buffer.add("M or F")
            return self.get_new_user()

        return {'sex': sex}

    def main(self):
        self.buffer.show()
        self.get_command()
        self.buffer.add(*self.user.read_messages(unique=True))
        World.save()
        self.buffer.show()
