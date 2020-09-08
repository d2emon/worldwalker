"""
Two Phase Game System
"""
import logging
from services.errors import CrapupError, GameStopped
from services.mud_exe import MudExeServices
from services.world import WorldService
from ..bbc import BBC
from ..tk import Talker
from .errors import CloseException, StopException, QuitException, ContinueException
from . import signals


class GameGo:
    def __init__(self, title, user):
        # Extra
        self.__in_fight = None

        # Game go
        self.services = MudExeServices
        self.user = user
        logging.debug("mud.exe %s %s", title, self.username)

        username = self.username
        print("Entering Game ....")
        self.bbc = BBC(
            tty=0,
            title=title,
            on_error=self.on_error,
            on_exit=self.on_exit,
            on_timer=self.on_timer,
        )
        print("Hello {}".format(username))
        self.services.post_log("GAME ENTRY: {}[{}]".format(username, self.user_id))
        self.talker = Talker(
            username,
            on_loose=self.on_loose,
            get_cmd=self.get_command,
            # show_buffer=self.bbc.show_buffer,
            output=self.bbc.add_buffer,
        )

    @property
    def title(self):
        if self.talker.player.visible > 9999:
            return "-csh"
        if self.talker.player.visible == 0:
            return "   --}}----- ABERMUD -----{{--     Playing as {}".format(self.username)
        return None

    @property
    def user_id(self):
        return self.user.get('user_id')

    @property
    def username(self):
        username = self.user.get('username')
        return "The {}".format(username) if username in ["Phantom"] else username

    def play(self):
        while True:
            try:
                self.bbc.run(self.talker.show)
            except CrapupError as e:
                return self.game_over(e)
            except GameStopped as e:
                return e

    def game_over(self, message):
        self.bbc.game_over()

        dashes = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        print()
        print(dashes)
        print()
        print(message)
        print()
        print(dashes)
        return 0

    # Events
    def on_error(self):
        self.talker.loseme()
        self.bbc.disconnect()
        raise GameStopped(255)

    def on_exit(self):
        print("^C")
        if self.__in_fight:
            return

        self.talker.loseme()
        raise CrapupError("Byeeeeeeeeee  ...........")

    def on_timer(self):
        with WorldService():
            self.bbc.events.interrupt = True
            self.talker.interrupt = self.bbc.events.interrupt

            self.talker.rte()

            self.bbc.events.interrupt = False
            self.talker.interrupt = self.bbc.events.interrupt

            # self.talker.on_time()
            # on_timing()
        self.bbc.reprint()

    # Talker events
    def get_command(self):
        self.bbc.show_bottom_screen(True)
        self.bbc.title = self.title
        command = self.bbc.show_command_prompt(self.talker.prompt)
        self.bbc.show_top_screen()

        self.bbc.add_buffer("<l>{}\n<\l>".format(command), True)
        return self.talker.process_command(command)

    def on_loose(self):
        self.bbc.events.is_active = False
