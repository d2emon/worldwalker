from .file_service import TextFileService


class Pfl(TextFileService):
    filename = "pfl"
    connections = dict()
    content = []
