import logging
from threading import Timer


SIGINT = 'SIGINT'
SIGTERM = 'SIGTERM'
SIGHUP = 'SIGHUP'
SIGTSTP = 'SIGTSTP'
SIGQUIT = 'SIGQUIT'
SIGCONT = 'SIGCONT'
SIGALRM = 'SIGALRM'


class SignalTimer:
    DEFAULT_INTERVAL = 2
    BLOCKED_INTERVAL = 2147487643

    def __init__(self, handler=lambda: None):
        self.__interval = None
        self.__handler = handler

        self.__interrupt = False
        self.__last_interrupt = 0

        self.__is_active = False
        self.__is_blocked = True

        self.__timer = Timer(self.BLOCKED_INTERVAL, self.on_timer)

    @property
    def time(self):
        return 0

    @property
    def interrupt(self):
        time = self.time
        if time - self.__last_interrupt > 2:
            self.__interrupt = True
        if self.__interrupt:
            self.__last_interrupt = time
        return self.__interrupt

    @interrupt.setter
    def interrupt(self, value):
        self.__interrupt = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        self.__is_active = value
        self.__is_blocked = not value
        if not value:
            self.__set_timer(self.BLOCKED_INTERVAL)
        else:
            self.__set_timer(self.DEFAULT_INTERVAL)

    @property
    def is_blocked(self):
        return self.__is_blocked

    @is_blocked.setter
    def is_blocked(self, value):
        self.__is_blocked = value
        if not value and self.__is_active:
            self.__set_timer(self.DEFAULT_INTERVAL)

    def __set_timer(self, interval):
        self.__interval = interval
        self.__timer.cancel()
        if interval != self.BLOCKED_INTERVAL:
            self.__timer = Timer(interval, self.on_timer)
            self.__timer.start()

    def on_timer(self):
        logging.debug('alarm: %s', self.__interval)

        if not self.__is_active:
            return

        if self.__is_blocked:
            return

        self.is_active = False
        self.__handler()
        self.is_active = True

        logging.debug("set timer %s", self.__interval)
        self.__set_timer(self.__interval)


class Events(SignalTimer):
    def __init__(
        self,
        on_error=lambda: None,
        on_exit=lambda: None,
        on_timer=lambda: None,
    ):
        super().__init__(on_timer)
        self.__signals = {
            SIGINT: on_exit,
            SIGTERM: on_exit,
            SIGHUP: on_error,
            SIGCONT: on_error,
            SIGALRM: self.on_timer,
        }

    def execute(self, signal, *args):
        logging.debug('%s: %s', signal, args)
        handler = self.__signals.get(signal)
        if handler is None:
            return
        handler()