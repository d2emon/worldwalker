from services.file_services.log_file import LogFile


def post(message):
    LogFile.log(message)
