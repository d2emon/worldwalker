from .file_service import FileService


class Exe(FileService):
    connections = dict()

    class FileStats:
        date = 100

    @classmethod
    def get_stats(cls):
        return cls.FileStats
