from .actions.action import Action, Special
from .actions.tk import StartGame
from .errors import ServiceError, CrapupError, CommandError
from .user import User
from .world import World


# Unknown
class Buffer:
    def __init__(self):
        self.__sysbuf = ""
        makebfr()

    def show(self):
        raise NotImplementedError()

    def add(self, *text, raw=False):
        if raw:
            self.__sysbuf += "".join(text)
        else:
            print("".join(text))


class Screen:
    def __init__(self, username, tty=0):
        self.tty = tty

        self.__key_buffer = ""

        self.user = User(username)
        self.buffer = Buffer()
        self.parser = Parser(self.user)

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
        # key_input(self.parser.prompt)[:80]
        # sig_aloff()
        return self.__key_buffer

    def set_progname(self, *args):
        raise NotImplementedError()

    # Tk
    def get_command(self):
        self.bottom()

        self.buffer.show()

        if self.user.player.visible > 9999:
            self.set_progname(0, "-csh")
        elif self.user.player.visible == 0:
            self.set_progname(0, "   --}----- ABERMUD -----{--     Playing as {}".format(self.user.name))

        work = self.__get_input()

        self.top()

        self.buffer.add("\001l{}\n\001".format(work), raw=True)

        World.load()
        self.buffer.add(*self.user.read_messages())

        if self.parser.parse(work) is None:
            return self.get_command()

    def main(self):
        self.buffer.show()
        self.get_command()
        self.buffer.add(*self.user.read_messages(unique=True))
        World.save()
        self.buffer.show()


class Parser:
    CONVERSATION_NONE = 0
    CONVERSATION_SAY = 1
    CONVERSATION_TSS = 2

    # Tk
    MODE_SPECIAL = 0
    MODE_GAME = 1

    # Unknown
    __PROMPT = {
        CONVERSATION_NONE: ">",
        CONVERSATION_SAY: "\"",
        CONVERSATION_TSS: "*",
    }
    __CONVERT = {
        CONVERSATION_NONE: "{}",
        CONVERSATION_SAY: "say {}",
        CONVERSATION_TSS: "tss {}",
    }

    def __init__(self, user):
        self.user = user
        self.user.on_message = self.__on_message

        # TK
        self.__conversation_mode = self.CONVERSATION_NONE
        self.__mode = self.MODE_SPECIAL
        # Unknown
        self.__debug_mode = False

        self.string_buffer = ""
        self.__word_buffer = ""
        self.__position = 0

        self.pronouns = {
            "it": "",
            "him": "",
            "her": "",
            "them": "",
            "there": "",
        }

        self.verbs = VerbsList()

    # Parse
    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = mode
        self.user.show_players = value == self.MODE_GAME

    # Tk
    @property
    def prompt(self):
        prompt = self.__PROMPT.get(self.__conversation_mode, "?")
        if self.user.is_wizard:
            prompt = "----" + prompt
        if self.__debug_mode:
            prompt = "#" + prompt
        if self.user.player.visible:
            prompt = "(" + prompt + ")"
        return prompt

    def __modify_action(self, action):
        if not action:
            return ""
        if action == "**" and self.__conversation_mode != self.CONVERSATION_NONE:
            self.__conversation_mode = self.CONVERSATION_NONE
            return None
        if action[0] == "*" and action != "*":
            return action[1:]
        return self.__CONVERT.get(self.__conversation_mode, "{}").format(action)

    def __on_message(self, message):
        # Print appropriate stuff from data block
        if self.__debug_mode:
            yield "\n<{}>".format(message.code)

    def parse(self, action):
        action = self.__modify_action(action)
        if action is None:
            return None

        result = action.lower() == ".q"
        if self.mode == self.MODE_GAME:
            self.__gamecom(self.user, action)
        elif not result:
            self.__special(self.user, action)

        self.user.check_fight()
        return result

    def start(self):
        self.user.reset_position()
        self.__special(self.user, ".g")
        self.user.in_setup = True

    # Parse
    def __iter__(self):
        return self

    def __next__(self):
        self.pronouns.update({
            "me": self.user.name,
            "myself": self.user.name,
        })

        for word in self.string_buffer[self.__position:].split(" "):
            self.__position += len(word) + 1
            self.__word_buffer += word
            if word:
                break
        self.__word_buffer = self.__word_buffer.lower()

        replace = self.pronouns.get(self.__word_buffer, None)
        if replace is not None:
            self.__word_buffer = replace

        if len(self.__word_buffer) <= 0:
            return None
        return self.__word_buffer

    def require_next(self, message):
        word = next(self)
        if word is None:
            raise CommandError(message)
        return word

    def full(self):
        text = self.string_buffer[self.__position:].trim()
        self.__position = len(self.string_buffer)
        return text

    def __gamecom(self, user, action):
        action = Action.prepare(self, action)
        if not action:
            return

        self.string_buffer = action
        self.__position = 0
        word = next(self)

        try:
            if word is None:
                raise CommandError("Pardon ?\n")

            verb = self.verbs.check(word)

            if verb is None:
                raise CommandError("I don't know that verb\n")

            yield from verb.execute(self, self.user)
        except CommandError as e:
            yield e
        except NotImplementedError as e:
            yield e

    # Tk
    def __special(self, user, action):
        action = Special.prepare(self, action)
        if not action:
            return
        elif action == "g":
            StartGame.action(self, self.user)
        else:
            print("\nUnknown . option\n")

    # Unknown
    def set_there(self, zone, location_id):
        self.pronouns['there'] = zone + " " + location_id

    # Unknown
    # For Actions
    def switch_debug(self):
        if not self.user.test_flag(4):
            return
        self.__debug_mode = not self.__debug_mode

    def start_game(self):
        self.mode = self.MODE_GAME
        self.user.show_players = True

        self.user.reset_location_id()
        self.user.initme()

        World.load()
        visible = 0 if not self.user.is_god else 10000
        self.user.player.start(self.user.NewUaf.strength, self.user.NewUaf.level, visible, self.user.NewUaf.sex)

        self.user.send_message(
            self.user,
            Message.WIZARD,
            self.user.location_id,
            "\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=self.user),
        )

        yield from self.user.read_messages(reset_after_read=True)
        self.user.go_to_channel(self.user.location_id)

        self.user.send_message(
            self.user,
            Message.GLOBAL,
            self.user.location_id,
            "\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=self.user),
        )

    def tss(self, action):
        World.save()

        keysetback()
        if getuid() != geteuid():
            raise CommandError("Not permitted on this ID\n")
        system(action)
        keysetup()

    def editor(self):
        show_buffer()
        World.save()

        try:
            chdir(ROOMS)
        except ServiceError:
            yield "Warning: Can't CHDIR\n"
        system("/cs_d/aberstudent/yr2/hy8/.sunbin/emacs")

    def honeyboard(self):
        system("/cs_d/aberstudent/yr2/hy8/bt")
