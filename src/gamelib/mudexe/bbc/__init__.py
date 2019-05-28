"""
Code for doing hardware windowed output on BBC GTSS terminals
Removed on UNIX version
"""
import logging
from services.bprintf import BufferService
from ..key import Key
from ..gamego.errors import CloseException, StopException, QuitException, ContinueException
from ..gamego.signals import Events, SIGALRM, SIGTERM, SIGTSTP, SIGQUIT, SIGCONT, SIGHUP, SIGINT


class BBC:
    def __init__(
        self,
        tty=0,
        title="",
        on_error=lambda: None,
        on_exit=lambda: None,
        on_timer=lambda: None,
    ):
        self.__tty = tty
        self.__title = title
        self.__buffer_id = BufferService.post_new_buffer()

        self.events = Events(
            on_error=on_error,
            on_exit=on_exit,
            on_timer=on_timer,
        )
        self.connect()
        self.init_screen()
        self.show_top_screen()

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if value is None:
            return

        # if self.args[n] == text:
        #     return
        #
        # y = len(self.args[n]) + len(self.args[1]) + 1
        # for x in range(y):
        #     self.args[n][x] = 0
        # self.args[n] = text
        logging.debug("set_progname(%s, %s)", 0, value)
        self.__title = value

    # Key
    @classmethod
    def connect(cls):
        Key.connect()

    @classmethod
    def disconnect(cls):
        Key.disconnect()

    def show_prompt(self, prompt):
        self.add_buffer(prompt)
        self.show_buffer()

    def reprint(self):
        Key.is_finished = True
        self.show_buffer()
        return Key.reprint()

    def get_input(self, prompt, max_length=80, on_input=lambda prompt: None):
        work = Key.get_input(prompt, max_length, self.show_prompt)
        # BufferService.post_buffer(self.__buffer_id, "<l>{}\n</l>".format(work))
        return work

    # Main BBC
    def init_screen(self):
        logging.debug("Init Screen[%s]", self.__tty)
        if self.__tty != 4:
            return

    def show_top_screen(self):
        logging.debug("Top Screen[%s]", self.__tty)
        print()
        print(self.title)
        print("/" + "-" * 80 + "\\")
        if self.__tty != 4:
            return

    def show_bottom_screen(self, with_buffer=False):
        if with_buffer:
            self.show_buffer()

        logging.debug("Bottom Screen[%s]", self.__tty)
        print()
        print("\\" + "-" * 80 + "/")
        if self.__tty != 4:
            return

        if with_buffer:
            self.show_buffer()

    def show_command_prompt(self, prompt):
        self.events.is_active = True
        command = self.get_input(prompt)
        #
        self.events.on_timer()
        #
        self.events.is_active = False
        return command

    # Main
    def run(self, action=lambda: None):
        try:
            self.show_buffer()
            # sendmsg(name);

            # self.get_cmd()
            action()
            self.show_buffer()

            self.events.execute(SIGALRM)
        except KeyboardInterrupt as e:
            self.events.execute(SIGINT, e)
        except (ValueError, SystemExit) as e:
            self.events.execute(SIGTERM, e)
        except CloseException as e:
            self.events.execute(SIGHUP, e)
        except StopException as e:
            self.events.execute(SIGTSTP, e)
        except QuitException as e:
            self.events.execute(SIGQUIT, e)
        except ContinueException as e:
            self.events.execute(SIGCONT, e)

    def game_over(self):
        self.show_buffer()
        Key.show_prompt = False  # So we dont get a prompt after the exit
        self.disconnect()

    # Buffer
    @property
    def is_dirty(self):
        # Unknown
        return BufferService.get_dirty(self.__buffer_id)

    @is_dirty.setter
    def is_dirty(self, value):
        # Unknown
        if value:
            BufferService.post_dirty(self.__buffer_id)

    def add_buffer(self, message, raw=False):
        # Unknown
        # bprintf()
        return BufferService.post_buffer(self.__buffer_id, message, raw)

    def get_buffer(self, is_finished=True):
        # Unknown
        # pbfr()
        return BufferService.get_buffer(self.__buffer_id, is_finished)

    def show_buffer(self, is_finished=True):
        self.events.is_blocked = True

        # WorldService.disconnect()

        # if len(sysbuf):
        #     Key.show_prompt = True
        # if len(sysbuf) and Key.is_finished:
        #     print()
        # Key.is_finished = False

        # if log_fl is not None:
        #     iskb = False
        #     dcprnt(sysbuf, log_fl)

        # if snoopd is not None:
        #     fln = opensnoop(Player.players[snoopd].player_id, "a")
        #     if fln > 0:
        #         iskb = False
        #         dcprnt(sysbuf, fln)
        #         fcloselock(fln)

        # iskb = True
        # dcprnt(sysbuf, stdout)
        # sysbuf = ""  # clear buffer

        # if snoopt is not None:
        #     viewsnoop()

        print(self.get_buffer(is_finished), end="")

        self.events.is_blocked = False
