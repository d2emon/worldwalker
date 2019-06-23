from datetime import datetime
from .buffer import Buffer
from .errors import CrapupError, ServiceError
from .keys import Keys
from .parser import Parser
from .player.user import User
from .world import World


class Screen:
    def __init__(self, username, tty=0):
        # Signals
        self.__active = False
        self.__last_interrupt = None
        self.__program_name = None

        Keys.on()

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
    def interrupt(self):
        time = datetime.now()
        if not self.__last_interrupt or (time - self.__last_interrupt).total_seconds() <= 2:
            return False
        self.__last_interrupt = time
        return True

    @property
    def program_name(self):
        return self.__program_name

    @program_name.setter
    def program_name(self, value):
        raise NotImplementedError()

    def block(self):
        self.__signal(SIGALRM, None)

    def unblock(self):
        self.__signal(SIGALRM, self.on_timer)

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
        self.__active = True
        value = Keys.get_command(self.parser.prompt, 80)
        self.__active = False
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
        }.get(Keys.get_sex())

        if sex is None:
            self.buffer.add("M or F")
            return self.get_new_user()

        return {'sex': sex}

    def main(self):
        while True:
            self.buffer.show()
            self.get_command()
            self.buffer.add(*self.user.read_messages(unique=True))
            World.save()
            self.buffer.show()

    def error_message(self, message):
        dashes = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        self.buffer.show()
        self.buffer.to_show = False  # So we dont get a prompt after the exit

        print("\n".join([
            "",
            dashes,
            "",
            message,
            "",
            dashes,
        ]))
        raise SystemExit(0)

    # Events
    def on_crapup(self, message):
        return self.error_message(message)

    def on_error(self):
        self.user.loose()
        raise SystemExit(255)

    def on_timer(self):
        if not self.__active:
            return

        self.__active = False
        World.load()

        self.parser.read_messages(*self.user.read_messages(interrupt=self.interrupt))
        self.user.on_time()

        World.save()
        Keys.reprint()
        self.__active = True

    def on_quit(self):
        print("^C\n")
        if self.user.in_fight:
            return

        self.user.loose()
        return self.error_message("Byeeeeeeeeee  ...........")
