from .file_service import FileService


def time():
    return 0


class ResetN(FileService):
    filename = "reset.n"
    connections = dict()
    started = 0

    @classmethod
    def get_data(cls, token, **kwargs):
        super().get_data(token, **kwargs)
        yield cls.started

    @classmethod
    def time(cls, token):
        return time() - next(cls.get_data(token))
