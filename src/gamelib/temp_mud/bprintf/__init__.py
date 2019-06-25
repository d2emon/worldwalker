from ..errors import CrapupError, LooseError, ServiceError
from ..services.snoops import SnoopsService
from ..syslog import syslog
from ..world import World


class Buffer:
    __MAX_LENGTH = 235
    __MAX_BUFFER = 4095

    def __init__(self):
        self.to_show = False  # pr_due
        self.break_line = False  # pr_qcr

        self.__buffer = ""

        self.__snoop_dest = None
        self.__snoop_target = None

    def add(self, message):
        if len(message) > self.__MAX_LENGTH:
            syslog("Bprintf Short Buffer overflow")
            raise CrapupError("Internal Error in BPRINTF")

        if len(message) + len(self.__buffer) > self.__MAX_BUFFER:
            syslog("Buffer overflow on user {}".format(user.name))
            raise LooseError("PANIC - Buffer overflow")

        self.__buffer += message

    def __get_buffer(self, user, from_keyboard=False):
        yield from user.decode(self.__buffer, from_keyboard)

    def __to_log(self, user, log):
        if log is None:
            return
        log.add(self.__get_buffer(user))

    def __to_snoop(self, user):
        if self.__snoop_dest is None:
            return
        try:
            SnoopsService.push(user=user.name, text=self.__get_buffer(user))
        except ServiceError:
            pass

    def show(self, game, log=None):
        game.active = False

        World.save()

        if self.__buffer:
            self.to_show = True
            if self.break_line:
                yield "\n"
        self.break_line = False

        self.__to_log(game.user, log)
        self.__to_snoop(game.user)
        yield from self.__get_buffer(game.user, True)

        # clear buffer
        self.__buffer = ""

        if self.__snoop_target is not None:
            yield from map(lambda s: "|" + s, SnoopsService.get(user=game.user.name))

        game.active = True
