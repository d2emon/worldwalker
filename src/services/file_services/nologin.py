from games.mud.exceptions import FileServiceError
from .file_service import FileService


class Nologin(FileService):
    filename = "nologin"
    connections = dict()
    content = None

    @classmethod
    def check(cls):
        """
        Check if there is a no logins file active

        :return:
        """
        try:
            with cls(permissions='r') as token:
                raise cls.get_content(token)
        except FileServiceError:
            return
