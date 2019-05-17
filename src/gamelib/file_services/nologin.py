from .file_service import TextFileService


class Nologin(TextFileService):
    connections = dict()
    content = None
