from .file_service import FileService


class Exe(FileService):
    filename = "mud.1"
    connections = dict()

    class FileStats:
        date = "01.01.1970 00:00"

    @classmethod
    def get_stats(cls):
        return cls.FileStats
