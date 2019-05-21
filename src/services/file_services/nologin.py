from .file_service import TextFileService


class Nologin(TextFileService):
    filename = "nologin"
    connections = dict()
    content = None
