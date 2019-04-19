from gamelib.services.message import Message
from ..console import Console
from ..database.world import World
from ..database.models.person import Person
from ..exceptions import GameException, CrapupException
from ..database.exceptions import NoWorldFileException
from .exceptions import DuplicateEntryException
from .special import SPECIAL_COMMANDS

from ..aber_parse import eorte
from ..aber_parse.parseGlobals import ParseGlobals


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

    def prepare(self):
        self.io = Console(self.user_id)

        self.message_id = None
        self.put_on()

        World.open()
        self.rte()
        World.close()

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

    def rte(self):
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


