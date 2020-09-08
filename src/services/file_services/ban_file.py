from ..errors import FileServiceError
from .file_service import FileService


class BanFile(FileService):
    filename = "ban_file"
    connections = dict()
    content = None

    @classmethod
    def check(cls, user_id):
        """
        Check to see if UID in banned list

        :return:
        """
        try:
            with cls(permissions="r+") as token:
                if user_id in list(cls.get_line(token, max_length=79)):
                    raise PermissionError("I'm sorry- that userid has been banned from the Game\n")
        except FileServiceError:
            return
