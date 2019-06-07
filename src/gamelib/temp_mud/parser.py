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
            self.buffer.add(*self.user.read_messages(reset_after_read=True))
            World.save()
        except ServiceError:
            raise CrapupError("Sorry AberMUD is currently unavailable")

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

        self.buffer.add("\001l{}\n\001".format(work), raw=True)

        World.load()
        self.buffer.add(*self.parser.read_messages())
        if self.parser.parse(work) is None:
            return self.send_message()

    def main(self):
        self.buffer.show()
        self.send_message()
        self.buffer.add(*self.parser.read_messages(True))
        World.save()
        self.buffer.show()


class Parser:
    CONVERSATION_NONE = 0
    CONVERSATION_SAY = 1
    CONVERSATION_TSS = 2

    MODE_SPECIAL = 0
    MODE_GAME = 1

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

        self.__conversation_mode = self.CONVERSATION_NONE
        self.mode = self.MODE_SPECIAL
        self.__debug_mode = False

        self.__special(self.user, ".g")
        self.user.in_setup = True

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

    # Unknown
    def __special(self, user, action):
        action = Special.prepare(self, action)
        if not action:
            return
        elif action == "g":
            StartGame.action(self, self.user)
        else:
            print("\nUnknown . option\n")

    def read_messages(self, unique=False):
        if unique and self.user.rd_qd:
            return

        yield from self.output_messages(*self.user.read_messages())

        if unique:
            self.user.rd_qd = False

    def output_messages(self, *messages):
        """
        Print appropriate stuff from data block

        :return:
        """
        for message in messages:
            if self.__debug_mode:
                yield "\n<{}>".format(message.code)
            yield from self.user.process_message(message)

    # For Actions
    def switch_debug(self):
        if not self.user.player.test_flag(4):
            return
        self.__debug_mode = not self.__debug_mode
