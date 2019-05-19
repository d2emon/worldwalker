from .file_service import TextFileService


class MotD(TextFileService):
    filename = "motd"
    connections = dict()
    content = [
        "Message of the day",
    ]
