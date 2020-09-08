from games.mud.exceptions import FileServiceError, MudError
from .file_service import FileService


class Exe(FileService):
    filename = "mud.1"
    connections = dict()

    class FileStats:
        date = "01.01.1970 00:00"

    @classmethod
    def get_stats(cls):
        return cls.FileStats

    @classmethod
    def get_created(cls):
        stats = cls.get_stats()
        return stats.date if stats is not None else "<unknown>\n"

    @classmethod
    def run(cls, *args):
        try:
            with cls() as token:
                cls.execute(token, *args)
        except FileServiceError:
            raise MudError("mud.exe : Not found\n")
