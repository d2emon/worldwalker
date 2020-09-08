from gamelib.services.message import Message
from gamelib.mudexe.temp.console import Console
from gamelib.mudexe.temp.database import World
from gamelib.mudexe.temp.database import Person

from gamelib.mudexe.temp.exceptions import GameException, CrapupException
from gamelib.services.buffer.exceptions import ShortBufferOverflowError, BufferOverflowError
from gamelib.mudexe.temp.database import NoWorldFileException
from .exceptions import DuplicateEntryException
from .special import SPECIAL_COMMANDS

from gamelib.mudexe.temp.used.aber_parse import eorte
from gamelib.mudexe.temp.used.aber_parse import ParseGlobals


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

        self.io = None

        self.is_on = False
        self.message_id = None
        self.person_id = 0
        self.location_id = 0
        self.last_update = 0
        self.in_setup = False
        self.mode = 0
        self.input_mode = 0  # convflg

        self.strength = 0
        self.level = 0
        self.sex = 0

        self.debug_mode = False

    def __str__(self):
        return self.name

    @property
    def person(self):
        return Person(self.person_id)

    def init_person(self):
        self.person.strength = self.strength
        self.person.level = self.level
        if self.level < 10000:
            self.person.vis = 0
        else:
            self.person.vis = 10000
        self.person.weapon = None
        self.person.sexall = self.sex
        self.person.helping = None

    def prepare(self):
        self.io = Console(self.user_id)

        self.message_id = None
        self.put_on()

        self.rte(save=True)

        self.message_id = None
        self.special(".g")

        self.in_setup = True

    def put_on(self):
        self.is_on = False

        World.open()

        if Person.fpbn(self.name) is not None:
            raise DuplicateEntryException()

        self.person_id = Person.find_empty_person()
        self.person.add_user(self)

        self.is_on = True

    @property
    def need_update(self):
        messages = self.message_id - self.last_update
        if messages < 0:
            messages = -messages
        return messages >= 10

    def update(self):
        if not self.need_update:
            return

        World.open()
        self.person.pos = self.message_id
        self.last_update = self.message_id

    def special(self, code_string):
        if code_string[0] != '.':
            return False
        code = code_string.lower()[1]

        special_command = SPECIAL_COMMANDS.get(code)
        if special_command is None:
            raise GameException("\nUnknown . option\n")
        special_command(self)
        return True

    def rte(self, save=False):
        try:
            World.open()

            if self.message_id is None:
                self.message_id = Message.last_id

            last_id = Message.last_id
            for message in Message.select(self.message_id, last_id):
                message.output(self)
            self.message_id = last_id

            self.update()
            eorte()

            ParseGlobals.rdes = 0
            ParseGlobals.tdes = 0
            ParseGlobals.vdes = 0
        except NoWorldFileException:
            raise CrapupException("AberMUD: FILE_ACCESS : Access failed\n")
        if save:
            World.close()

    @property
    def prompt(self):
        mode_flag = {
            0: ">",
            1: "\"",
            2: "*",
        }

        result = "\n"

        if self.debug_mode:
            result += "#"

        if self.level > 9:
            result += "----"

        result += mode_flag.get(self.input_mode, "?")

        if self.person.vis:
            return "({})".format(result)
        return result

    def add_text(self, text):
        try:
            self.io.send(text)
        except ShortBufferOverflowError:
            # syslog("Bprintf Short Buffer overflow")
            raise CrapupException("Internal Error in BPRINTF")
        except BufferOverflowError:
            # loseme()
            # syslog("Buffer overflow on user {}".format(str(self)))
            raise CrapupException("PANIC - Buffer overflow")
