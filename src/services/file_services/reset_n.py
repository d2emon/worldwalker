from .file_service import FileService


class ResetN(FileService):
    filename = "reset.n"
    connections = dict()
    started = 0

    @classmethod
    def get_data(cls, token, **kwargs):
        super().get_data(token, **kwargs)
        yield cls.started

    @classmethod
    def get_time(cls):
        with cls(permissions='r') as token:
            return next(cls.get_data(token))
