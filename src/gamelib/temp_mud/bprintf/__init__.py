import logging
from ..errors import CrapupError, LooseError, ServiceError
from ..services.buffer import BufferService, BufferOverflowError, ShortBufferOverflowError
from ..services.snoops import SnoopsService
# from ..world import World


class Buffer:
    def __init__(self):
        self.__buffer_id = self.__put()

        self.__to_show = False  # pr_due
        self.__break_line = False  # pr_qcr

        self.__snoop_dest = None
        self.__snoop_target = None

    @classmethod
    def __put(cls):
        logging.debug("PUT buffer")
        return BufferService.put().get('buffer_id')

    def __clear(self):
        # clear buffer
        logging.debug("CLEAR buffer(%s)", self.__buffer_id)
        return BufferService.push_clear(
            buffer_id=self.__buffer_id,
        ).get('result', False)

    def __post(self, text, raw=False):
        logging.debug("POST buffer(%s):\t%s", self.__buffer_id, text)
        if raw:
            text = "\001l{}\n\001".format(text)
        try:
            return BufferService.post(
                buffer_id=self.__buffer_id,
                text=text,
            ).get('result', False)
        except ShortBufferOverflowError as e:
            raise CrapupError(e)
        except BufferOverflowError as e:
            raise LooseError(e)

    def __get(self, clear=True):
        logging.debug("GET buffer(%s)", self.__buffer_id)
        text = BufferService.get(
            buffer_id=self.__buffer_id,
        ).get('text', '')
        if clear:
            self.__clear()
        return text

    def add(self, *messages, raw=False):
        return [self.__post(message, raw) for message in messages]

    @classmethod
    def __to_log(cls, user, text):
        if user.log_service is None:
            return
        user.log_service.add(text)

    def __to_snoop(self, user, text):
        if self.__snoop_dest is None:
            return
        try:
            SnoopsService.push(user=user.name, text=text)
        except ServiceError:
            pass

    def show(self, game):
        game.active = False

        # World.save()

        text = self.__get()
        if text:
            self.__to_show = True
            if self.__break_line:
                yield "\n"
        self.__break_line = False

        decoded = game.user.decode(text, False)
        self.__to_log(game.user, decoded)
        self.__to_snoop(game.user, decoded)

        yield game.user.decode(text, True)

        if self.__snoop_target is not None:
            yield from map(lambda s: "|" + s, SnoopsService.get(user=game.user.name))

        game.active = True

    def reprint(self, value):
        if not self.__to_show:
            return

        print(value)
        self.__to_show = False
