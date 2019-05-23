from .file_services import LogFile


class MudExeServices:
    @classmethod
    def post_log(cls, message):
        LogFile.log(message)
