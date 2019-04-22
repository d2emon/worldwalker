from ...mudexe.exceptions import CrapupException


class OutOfMemoryError(Exception):
    def __init__(self):
        super().__init__("Out Of Memory")


class ShortBufferOverflowError(CrapupException):
    pass


class BufferOverflowError(CrapupException):
    pass
