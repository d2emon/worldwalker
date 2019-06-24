from .actions import VerbsList
from .actions.action import Action, Special
from .actions.tk import StartGame
from .errors import CommandError
from .item.items import find_item
from .world import World


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
        self.mode = self.MODE_SPECIAL
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
        return self.MODE_GAME if self.user.show_players else self.MODE_SPECIAL

    @mode.setter
    def mode(self, value):
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

    def get_item(self):
        return self.user.get_item(
            self.require_next("Tell me more ?\n"),
            error_message="There isn't one of those here\n",
        )

    def get_target(self, here=True):
        # This one isn't for magic
        player_name = self.require_next("Who ?\n")
        if player_name == "at":
            return self.get_target(here)  # STARE AT etc

        World.load()
        target = Player.find(player_name)
        if target is None:
            raise CommandError("Who ?\n")

        if here and target.location.location_id != self.user.location_id:
            raise CommandError("They are not here\n")
        return target

    def get_number(self, min_value=0, max_value=None):
        value = int(self.require_next("Missing numeric argument\n"))
        if min_value is not None and value < min_value:
            raise CommandError("Invalid range\n")
        if max_value is not None and value > max_value:
            raise CommandError("Invalid range\n")
        return value
